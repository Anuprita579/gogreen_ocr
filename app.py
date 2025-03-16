from flask import Flask, request, jsonify
import easyocr
from PIL import Image
import io
import os

app = Flask(__name__)

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])  # Add languages as needed

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
        image = Image.open(io.BytesIO(image_bytes))

        # Extract text using EasyOCR
        extracted_text = reader.readtext(image_bytes, detail=0)

        return jsonify({"extracted_text": extracted_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render uses dynamic ports
    app.run(host='0.0.0.0', port=port)
