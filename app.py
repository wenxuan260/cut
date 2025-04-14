from flask import Flask, request, send_file
import cv2
import numpy as np
import io

app = Flask(__name__)

@app.route("/")
def home():
    return "OpenCV Image Crop API is running!"

@app.route("/crop", methods=["POST"])
def crop_image():
    if "image" not in request.files:
        return {"error": "No image uploaded"}, 400

    file = request.files["image"]
    img_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return {"error": "Invalid image file"}, 400

    # 💡 只保留图片上部的 2300 像素高度
    cropped_img = img[:2300, :]

    # 转成 PNG 二进制
    _, buffer = cv2.imencode('.png', cropped_img)
    io_buf = io.BytesIO(buffer)

    return send_file(io_buf, mimetype='image/png')
