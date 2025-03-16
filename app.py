from flask import Flask, request, jsonify
import io
from PIL import Image
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Lazy loading of OCR reader
reader = None

def get_reader():
    global reader
    if reader is None:
        import easyocr
        reader = easyocr.Reader(['en'])
    return reader

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "online",
        "message": "OCR API is running. Send POST requests to /ocr endpoint with an image file."
    })

@app.route('/ocr', methods=['POST'])
def ocr_text():
    if 'image' not in request.files:
        return jsonify({"error": "No image file found"}), 400
        
    file = request.files['image']
        
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    try:
        # Convert image to bytes
        image_bytes = file.read()
        
        # Get reader lazily
        reader = get_reader()
        
        # Extract text using EasyOCR
        extracted_text = reader.readtext(image_bytes, detail=0)
        
        return jsonify({"extracted_text": extracted_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Changed default to 10000 to match what Render seems to be using
    app.run(host='0.0.0.0', port=port)