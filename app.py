from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

# Set Tesseract Path (only needed for Windows users)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.route('/ocr', methods=['POST'])
def ocr_text():
    if 'image' not in request.files:
        return jsonify({"error": "No image file found"}), 400

    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Save the file temporarily
        image_path = os.path.join("temp_image.jpg")
        file.save(image_path)

        # Open and process the image
        image = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(image)

        # Remove temporary file
        os.remove(image_path)

        return jsonify({"extracted_text": extracted_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

