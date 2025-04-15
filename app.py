from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np

app = Flask(__name__)

@app.route("/crop", methods=["POST"])
def crop_image():
    data = request.json
    image_base64 = data.get("imageBase64")
    if not image_base64:
        return jsonify({"error": "No imageBase64 provided"}), 400

    # 解码 base64 图片
    try:
        image_data = base64.b64decode(image_base64)
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        return jsonify({"error": f"Failed to decode image: {str(e)}"}), 400

    # 剪裁图片上方 2300 像素区域
    cropped_img = img[:2300, :]

    # 再编码回 base64
    _, buffer = cv2.imencode(".png", cropped_img)
    cropped_base64 = base64.b64encode(buffer).decode("utf-8")

    return jsonify({"cropped_image_base64": cropped_base64})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

