from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/detect', methods=['POST'])
def detect_bird():
    # This is a stub that always returns false
    # In a real implementation, you would process the image and perform detection
    return jsonify({"bird_detected": False})


if __name__ == '__main__':
    app.run(debug=True, port=9001)
