
from uuid import uuid4

from flask import Flask,request
from flask_cors import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token
from flask_jwt_extended import JWTManager

import json
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
# import rsa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import MEDIUMTEXT



app = Flask(__name__, static_folder='dist', static_url_path='/')
app.config["SECRET_KEY"] = "BoogieIsland"
app.config['SQLALCHEMY_DATABASE_URI']='mysql://boogiepan:BoogiePan@localhost:3306/boogiepan' 
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app, supports_credentials=True)
jwt = JWTManager(app)
db = SQLAlchemy(app)


class User(db.Model):
    ___tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    client_random = db.Column(db.String(120))
    master_key_enc = db.Column(db.Text)
    derived_auth_key_hashed = db.Column(db.String(120))
    rsa_private_key_enc = db.Column(db.Text)
    rsa_public_key = db.Column(db.Text)


class File(db.Model):
    file_id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer)
    name = db.Column(db.String(120))
    type = db.Column(db.String(120))
    uuid = db.Column(db.String(120))
    size_mb = db.Column(db.FLOAT)

    # file_sha256 = db.Column(db.String(120))

    def to_json(self):
        return {
            'file_id': self.file_id,
            'user': self.user,
            'name': self.name,
            'type': self.type,
            'uuid': self.uuid,
            'size_mb': f"{round(self.size_mb, 2)} MB" if round(self.size_mb,
                                                               2) != 0 else f"{round(self.size_mb * 1024, 2)} KB"
        }


class FileContent(db.Model):
    uuid = db.Column(db.String(120), primary_key=True)
    file_enc_key = db.Column(db.TEXT)
    content = db.Column(MEDIUMTEXT)

    def to_json(self):
        return {
            'uuid': self.uuid,
            'file_enc_key': self.file_enc_key,
            'content': self.content
        }


@app.route('/api/verify_token', methods=['POST'])
# 使用jwt_required修饰器保证用户是在登录状态下操作
@jwt_required()
def verify_token():
    return json.dumps({"identity": get_jwt_identity()})


@app.route('/api/upload', methods=['POST'])
# 使用jwt_required修饰器保证用户是在登录状态下操作
@jwt_required()
def upload():
    raw = request.data
    json_data = json.loads(raw)
    encrypted = json_data['encrypted']
    file_enc_key = json_data['file_key']
    name = json_data['name']
    type = json_data['type']

    size_mb = len(encrypted) / 1024 / 1024

    # 判断encrypted大小是否大于15M
    # 判断标准为15而不是10M，因为加密后会有冗余
    if (size_mb > 15):
        return json.dumps({"errors": [{"file": "文件过大"}]}), 500

    # 存储至数据库
    try:
        uuid = str(uuid4())
        file = File(name=name, type=type, size_mb=size_mb,
                    uuid=uuid, user=get_jwt_identity())
        db.session.add(file)
        file_content = FileContent(uuid=uuid, content=encrypted, file_enc_key=file_enc_key)
        db.session.add(file_content)
        db.session.commit()
    except Exception as e:
        return json.dumps({"errors": [{"db": ["数据库错误", str(e)]}]}), 500

    return "上传成功"


@app.route('/api/download', methods=['POST'])
# 使用jwt_required修饰器保证用户是在登录状态下操作
@jwt_required()
def download():
    json_data = json.loads(request.data)
    file_id = json_data['id']

    # 判断文件是否存在
    file = File.query.filter_by(file_id=file_id).first()
    if not file:
        return json.dumps({'errors': {file: ["文件不存在"]}}), 500

    # 判断文件是否属于该用户
    if file.user != get_jwt_identity():
        return json.dumps({'errors': {file: ["无下载权限"]}}), 500

    # 获取文件内容
    file_content = FileContent.query.filter_by(uuid=file.uuid).first()
    return json.dumps(file_content.to_json())


# 实现匿名用户下载加密文件
@app.route('/api/download_original', methods=['POST'])
# 这里没有jwt_required
def download_original():
    json_data = json.loads(request.data)
    file_id = json_data['id']

    # 判断文件是否存在
    file = File.query.filter_by(file_id=file_id).first()
    if not file:
        return json.dumps({'errors': {file: ["文件不存在"]}}), 500

    # 获取文件内容
    file_content = FileContent.query.filter_by(uuid=file.uuid).first()
    return json.dumps(file_content.to_json())


# 下载加密文件对应的签名文件
@app.route('/api/download_signature', methods=['POST'])
def download_signature():
    # 在这里实现数字签名文件的生成和下载逻辑
    # 这部分应该不是我做？
    # 返回数字签名文件内容
    return json.dumps({'signature_file_content': '这里是数字签名文件的内容'})





if __name__ == '__main__':
   app.run(debug=True)

