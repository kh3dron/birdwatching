import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
import os

from flask import Flask, request, jsonify
from flask_cors import CORS

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


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/detect', methods=['POST'])
def detect_bird_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected image file'}), 400

    # Save the uploaded image temporarily
    temp_path = 'temp_image.jpg'
    image_file.save(temp_path)

    # Load the model
    model = load_model()

    # Preprocess the image
    img_array = preprocess_image(temp_path)

    # Detect bird
    is_bird, probability = detect_bird(model, img_array)

    # Remove the temporary image file
    os.remove(temp_path)

    return jsonify({
        'is_bird': is_bird,
        'probability': float(probability)
    })

if __name__ == '__main__':
    app.run(debug=True, port=9001)
