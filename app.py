from flask import Flask, request, jsonify
from PIL import Image
import base64
import cv2
import numpy as np
import io

app = Flask(__name__)

@app.route('/')
def home():
    return 'Flask OCR Crop API is running!'

@app.route('/crop', methods=['POST'])
def crop_image():
    try:
        data = request.get_data()
        #img_bytes = base64.b64decode(data)
        img_arr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({'error': 'Invalid image'}), 400

        cropped_img = img[:2300, :]
        _, buffer = cv2.imencode('.png', cropped_img)
        cropped_base64 = base64.b64encode(buffer).decode('utf-8')

        return cropped_base64  # 不加前缀，方便 AI Builder 识别
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cropbase64', methods=['POST'])
def crop_base64_image():
    try:
        data = request.get_data()
        img_bytes = base64.b64decode(data)
        img_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({'error': 'Invalid image'}), 400

        cropped_img = img[:2300, :]
        _, buffer = cv2.imencode('.png', cropped_img)
        cropped_base64 = base64.b64encode(buffer).decode('utf-8')

        return cropped_base64  # 不加前缀，方便 AI Builder 识别
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cut_image', methods=['POST'])
def cut_image():
    img_data = request.get_data()
    img = Image.open(io.BytesIO(img_data))
 
    cropped = img.crop((0, 0, 100, 100))

    output = io.BytesIO()
    cropped.save(output, format='PNG')
    base64_img = base64.b64encode(output.getvalue()).decode('utf-8')
    return base64_img

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


