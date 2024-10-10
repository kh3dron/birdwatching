import time
import json
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import (
    InceptionV3,
    preprocess_input,
    decode_predictions,
)
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
import os
import cv2
import base64
import logging
import datetime

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

bird_wordlist = open("labels.txt", "r").readlines()
bird_wordlist = [e.strip() for e in bird_wordlist]


def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(299, 299))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array


# if a bird is in the top 10 predictions, call that a bird predicted
# false positives are ok for now
def detect_bird(model, img_array):
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=20)[0]

    for _, label, probability in decoded_predictions:
        if label in bird_wordlist:
            print(f"[***] bird detected: {label}")
            return True, probability, label

    most_probable = decoded_predictions[0]
    return False, most_probable[2], most_probable[1]


# take a picture with the webcam, inference, and save accordingly
def camcheck(model):

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap.open(0)
        return
    ret, frame = cap.read()
    if not ret:
        logger.error("Failed to capture frame from webcam")
        return
    cap.release()

    # decrease brightness, helps bright sunlight effect. TODO fix better
    brightness = 0.9
    frame = cv2.convertScaleAbs(frame, alpha=brightness, beta=0)

    # Add timestamp to the bottom left corner
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(
        frame,
        timestamp,
        (10, frame.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 0),
        1,
    )

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb_frame).resize((299, 299))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    logger.info("[*] Starting inference...")
    is_bird, probability, label = detect_bird(model, img_array)
    logger.info("[*] Inference complete")
    print(f"[*] Inference complete, found: {label}")

    _, buffer = cv2.imencode(".jpg", frame)
    image_data = base64.b64encode(buffer).decode("utf-8")

    if is_bird:
        try:
            os.makedirs("../found", exist_ok=True)
            filename = time.strftime("%Y-%m-%d--%H-%M-%S") + f"-{label}" + ".mp4"
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(f"../found/{filename}", fourcc, 20.0, (frame.shape[1], frame.shape[0]))

            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                cap.open(0)
                return

            logger.info("[*] Bird found! Recording video for 5 seconds...")
            start_time = time.time()
            while (time.time() - start_time) < 5:  # Record for 5 seconds
                ret, frame = cap.read()
                if not ret:
                    logger.error("Failed to capture frame from webcam")
                    break
                out.write(frame)

            cap.release()
            out.release()
            logger.info(f"Bird video saved: {filename}")
            
        except Exception as e:
            logger.error(f"Failed to save bird video: {e}")

    try:
        os.makedirs("../static", exist_ok=True)
        with open("../static/latest.jpg", "wb") as image_file:
            image_file.write(base64.b64decode(image_data))
        logger.info("Latest image saved")

        with open("../static/label.json", "w") as label_file:
            json.dump(
                {"is_bird": is_bird, "probability": float(probability), "label": label},
                label_file,
            )
        logger.info("Label JSON saved")
    except Exception as e:
        logger.error(f"Failed to save static files: {e}")

    return


@tf.function(reduce_retracing=True)
def predict_wrapper(model, img_array):
    return model.predict(img_array)


if __name__ == "__main__":
    model = InceptionV3(weights="imagenet")
    while True:
        camcheck(model)
        time.sleep(0.5)
