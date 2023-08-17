import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS  # 导入 flask-cors 扩展

app = Flask(__name__)
CORS(app)  # 配置跨域请求

UPLOAD_FOLDER = 'upload'  # 设置上传文件保存的目录
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # 允许上传的文件类型

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'fileData' not in request.files:  # 修改这里的字段名
        return jsonify({'error': 'No file part'})

    file = request.files['fileData']  # 修改这里的字段名

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully'})
    else:
        return jsonify({'error': 'File type not allowed'})


@app.route('/api/files', methods=['GET'])
def get_files():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        files.append({'filename': filename, 'size': size})
    return jsonify(files)

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
