from flask import Flask, request, send_file
import cv2
import numpy as np
import io
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Binary Image Crop API is running!"

@app.route("/crop", methods=["POST"])
def crop_image():
    # 🔥 从原始请求体中读取图像字节
    img_bytes = request.get_data()
    img_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

    if img is None:
        return {"error": "Invalid image"}, 400

    # ✂️ 裁剪上方 2300 像素
    cropped_img = img[:2300, :]

    # ⏳ 转为 PNG 二进制返回
    _, buffer = cv2.imencode('.png', cropped_img)
    io_buf = io.BytesIO(buffer)

    return send_file(io_buf, mimetype='image/png')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
