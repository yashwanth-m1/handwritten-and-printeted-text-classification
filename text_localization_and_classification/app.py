import os
from flask import Flask, render_template, request, send_from_directory, jsonify
from classifier import load_classifier, classify_image
import cv2
import base64

app = Flask(__name__, static_folder='static', template_folder='templates')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = load_classifier()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    # Process image
    processed_img, results = classify_image(filepath, model)
    
    if processed_img is None:
        return jsonify({"error": "Processing failed"}), 500
    
    # Convert processed image to base64 to send back to frontend
    _, buffer = cv2.imencode('.png', processed_img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return jsonify({
        "image": img_base64,
        "results": results
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
