import datetime
import json
import jwt
from flask import Flask, request, jsonify, g
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

app = Flask(__name__)

# 模拟数据库表
class User:
    def __init__(self, user_id, email, rsa_public_key):
        self.user_id = user_id
        self.email = email
        self.rsa_public_key = rsa_public_key

class File:
    def __init__(self, file_id, user):
        self.file_id = file_id
        self.user = user

class ShareInfo:
    def __init__(self, share_id, user_id, file_id, download_count):
        self.share_id = share_id
        self.user_id = user_id
        self.file_id = file_id
        self.download_count = download_count

# 辅助函数
def get_user_by_id(user_id):
    # 根据用户ID从数据库获取用户信息
    return User(user_id, "user@example.com", "public_key")

def get_file_by_id(file_id):
    # 根据文件ID从数据库获取文件信息
    return File(file_id, get_user_by_id(1))

def get_share_info(user_id, file_id):
    # 根据用户ID和文件ID从数据库获取分享信息
    return ShareInfo(1, user_id, file_id, 5)

# 路由处理
@app.route('/api/share', methods=['POST'])
@jwt_required()
def share_file():
    json_data = request.get_json()
    share_user_id = get_jwt_identity()
    file_id = json_data['file_id']
    file = get_file_by_id(file_id)

    if file.user.user_id != share_user_id:
        return jsonify({'errors': {"file": ["无操作权限"]}}), 422

    share_info = get_share_info(share_user_id, file_id)
    if not share_info:
        return jsonify({'errors': {"file": ["文件未被分享"]}}), 500

    # 设置分享参数在JSON数据中，并创建JWT令牌
    json_data["share_user"] = get_user_by_id(share_user_id).email
    json_data["share_file_id"] = file_id
    json_data["created_timestamp"] = int(datetime.datetime.now().timestamp() * 1000)
    json_data["expired_days"] = 7  # 设置过期时间（例如，7天）
    share_token = create_access_token(identity=json_data, expires_delta=False)

    return jsonify({"share_token": share_token}), 200

@app.route('/api/share_info', methods=['POST'])
def get_share_info():
    json_data = request.get_json()
    jwt_token = json_data['share_token']
    try:
        idt = jwt.decode(jwt_token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'errors': {"expired": ["分享链接已过期"]}}), 422

    share_user = get_user_by_id(idt["share_user"])
    idt["rsa_public_key"] = share_user.rsa_public_key if idt.get('share_rsa_pk') else None

    share_info = get_share_info(share_user.user_id, idt["share_file_id"])
    if not share_info:
        return jsonify({'errors': {"file": ["文件未被分享"]}}), 500

    idt["count_left"] = share_info.download_count
    idt['share_file_id'] = create_access_token(identity=idt['share_file_id'])

    return jsonify(idt), 200

@app.route('/api/share_download', methods=['POST'])
def share_download():
    json_data = request.get_json()
    share_file_id = json_data["share_file_id"]
    share_info = get_share_info(g.user.user_id, share_file_id)
    if not share_info:
        return jsonify({'errors': {"file": ["文件未被分享"]}}), 500

    if share_info.download_count == 0:
        return jsonify({'errors': {"file": ["已经达到下载次数，不可下载"]}}), 500

    file = get_file_by_id(share_file_id)
    if not file:
        return jsonify({'errors': {"file": ["文件不存在"]}}), 500

    # 减少下载次数
    share_info.download_count -= 1

    # 下载文件内容（在这里仅模拟一个简单的字符串）
    file_content = "This is the content of the file with ID " + str(share_file_id)

    return jsonify({"content": file_content}), 200

if __name__ == '__main__':
    app.run(debug=True)
