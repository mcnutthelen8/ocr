from flask import Flask, request, jsonify
import easyocr
import requests
from io import BytesIO
from PIL import Image

app = Flask(__name__)
reader = easyocr.Reader(['en'])

@app.route('/ocr', methods=['GET'])
def ocr():
    image_url = request.args.get('url')
    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400
    
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    
    result = reader.readtext(img)
    text = ' '.join([res[1] for res in result])
    
    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(debug=True)
