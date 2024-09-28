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

from flask import Flask, request, jsonify
from flask_cors import CORS

bird_wordlist = open("labels.txt", "r").readlines()
bird_wordlist = [e.strip() for e in bird_wordlist]


def load_model():
    # Load pre-trained InceptionV3 model
    model = InceptionV3(weights="imagenet")
    return model


def preprocess_image(img_path):
    # Load and preprocess the image
    img = image.load_img(img_path, target_size=(299, 299))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array


def detect_bird(model, img_array):
    # Make predictions
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=10)[0]

    for _, label, probability in decoded_predictions:
        # print(f"[*] label: {label}, probability: {probability}")
        if label in bird_wordlist:
            print(f"[***] bird detected: {label}")
            return True, probability, label

    most_probable = decoded_predictions[0]
    return False, most_probable[2], most_probable[1]


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route("/")
def index():
    return "A-OK"

@app.route("/detect", methods=["GET"])
def detect_bird_route():
    print("[*] Starting inference...")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap.open(0)  # Try to open the camera again

    if not cap.isOpened():
        return (
            jsonify(
                {
                    "error": "Cannot open webcam. Please check your camera connection and permissions."
                }
            ),
            500,
        )

    ret, frame = cap.read()
    if not ret:
        return jsonify({"error": "Failed to capture image from webcam."}), 500

    cv2.imwrite("webcam_photo.jpg", frame)

    # Load the model
    model = load_model()

    # Preprocess the image
    img_array = preprocess_image("webcam_photo.jpg")

    # Detect bird
    is_bird, probability, label = detect_bird(model, img_array)

    # Read the image file and encode it to base64
    with open("webcam_photo.jpg", "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    # Remove the temporary image file
    # os.remove("webcam_photo.jpg")
    print("[*] Inference complete")
    return jsonify(
        {
            "is_bird": is_bird,
            "probability": float(probability),
            "label": label,
            "image_data": image_data,
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=9111, host="0.0.0.0")
