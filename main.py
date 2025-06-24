from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64

app = Flask(__name__)
CORS(app)

def imagem_base64(img):
    _, buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(buffer).decode('utf-8')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400

    file = request.files['image']
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({'erro': 'Erro ao ler a imagem'}), 500
    img_resized = cv2.resize(img, (30,30))
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

    imagens_base64 = {
        'original': imagem_base64(img_resized),
        'cinza': imagem_base64(img_gray),
    }

    return jsonify(imagens_base64)

if __name__ == '__main__':
    app.run(debug=True)

##Desenvolvimento de um site educacional (React + Flask) que ajude no aprendizado sobre visão computacional. 