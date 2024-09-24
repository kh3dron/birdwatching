import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
import os

bird_wordlist = open('labels.txt', 'r').readlines()
bird_wordlist = [e.strip() for e in bird_wordlist]
def load_model():
    # Load pre-trained InceptionV3 model
    model = InceptionV3(weights='imagenet')
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
        if label in bird_wordlist:
            return True, probability
    
    return False, 0.0

def main():
    model = load_model()
    
    # Replace with the path to your image
    test_dir = 'birds'

    for e in os.listdir(test_dir):
        img_path = os.path.join(test_dir, e)
        img_array = preprocess_image(img_path)
        
        print()
        print(img_path)
        is_bird, probability = detect_bird(model, img_array)
    
        if is_bird:
            print(f"A bird was detected in the image with {probability:.2%} confidence.")
        else:
            print("No bird was detected in the image.")

if __name__ == "__main__":
    main()