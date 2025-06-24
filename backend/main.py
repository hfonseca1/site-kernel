from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import io
import base64

app = Flask(__name__)
CORS(app)

def imagem_para_base64(img):
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

    # Processamentos: Original, Cinza, Borrado, Bordas
    img_original = img
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img, (15, 15), 0)
    img_edges = cv2.Canny(img, 100, 200)

    # Como cv2.imencode espera 3 canais, vamos converter as imagens que estão com 1 canal
    img_gray_3ch = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    img_edges_3ch = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2BGR)

    # Converter todas para Base64
    imagens_base64 = {
        'original': imagem_para_base64(img_original),
        'cinza': imagem_para_base64(img_gray_3ch),
        'blur': imagem_para_base64(img_blur),
        'bordas': imagem_para_base64(img_edges_3ch)
    }

    return jsonify(imagens_base64)

if __name__ == '__main__':
    app.run(debug=True)
