
# 实现文件分享功能
<img src=功能清单.png>
## 一、具体工作内容

### 1. 分享者发起分享请求，设定分享参数
  
  - 数据库中存储分享信息的 Shareinfo 表：
    
    | Name           | Type    | Primary Key | Unique | Foreign Key |
    |:--------------:|:-------:|:-----------:|:------:|:-----------:|
    | share_id       | Integer | True        | True   | False       |
    | user_id        | Integer | False       | False  | True        |
    | file_id        | Integer | False       | False  | True        |
    | download_count | Integer | False       | False  | False       |




- 检查用户是否有操作权限。
  ```
    if file.user.user_id != share_user_id:
        return jsonify({'errors': {"file": ["无操作权限"]}}), 422
  ```
- 检查文件是否存在。
  ```
    if not file:
        return jsonify({'errors': {"file": ["文件不存在"]}}), 500
  ```
### 2. 分享者发起分享请求时，通过POST请求将分享信息（file_id等）放在JSON数据中，然后使用JWT编码生成一个令牌（share_token）。此时，JWT的payload（即令牌中的数据）包含了分享的相关参数，并签名得到share_token。
  ```
  json_data = json.loads(request.data)
  json_data["share_user"] = User.query.filter_by(user_id=get_jwt_identity()).first().email
  share_token = create_access_token(identity=json_data, expires_delta=False)
  ```
### 3. 前端将share_token作为分享口令展示给其他用户。
  ```
    return jsonify({"share_token": share_token}), 200
  ```
### 4. 下载者访问分享链接并发送分享口令share_token。
  ```
@app.route('/api/share_info', methods=['POST'])
def get_share_info():
    json_data = request.get_json()
    jwt_token = json_data['share_token']
  ```

- 判断时间是否过期。
  ```
    try:
        idt = jwt.decode(jwt_token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'errors': {"expired": ["分享链接已过期"]}}), 422
  ```
### 5. 后端根据分享信息验证下载条件是否符合（如文件是否存在、是否达到下载次数等）。
  ```
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
  ```
### 若符合下载条件，返回文件内容给下载者，同时更新分享信息中的下载次数。
- 减少下载次数
  ```
    share_info.download_count -= 1
  ```
- 获取文件内容
  ```
  file_content = FileContent.query.filter_by(uuid=file.uuid).first()
  ```

- 返回文件信息
  
  ```python
  return json.dumps({"content": file_content.to_json()["content"]})
  ```

通过JWT编码，可以在令牌中加入一些自定义的数据，这样可以在不存储session的情况下，实现对用户身份和权限的验证，同时保证了令牌的完整性和不可篡改性。这种无状态的验证方式使得服务器扩展变得更加容易。
## 二、实验中遇到的问题及解决方法

1. 报错：`ImportError: cannot import name 'jwt_required' from 'flask_jwt_extended'`
错误原因：这个报错是由于在 `from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required` 中使用了 `jwt_required`，但 `jwt_required` 并未从 `flask_jwt_extended` 中导入。
解决方法：确保 `flask_jwt_extended` 包已正确安装，并从 `flask_jwt_extended` 中导入 `jwt_required`。

2. 报错：`AttributeError: 'Flask' object has no attribute 'config'`
错误原因：这个报错是由于在代码中使用了 `app.config['SECRET_KEY']`，但是 `app` 对象并没有定义 `config` 属性。
解决方法：在代码中确保已为 `app` 对象设置了正确的 Flask 配置。在 `app` 对象创建之后，添加如下配置：`app.config['SECRET_KEY'] = 'your_secret_key_here'`。

3. 报错：`TypeError: 'NoneType' object is not subscriptable`
错误原因：这个报错可能出现在 `share_file()` 函数的 `file.user.user_id != share_user_id` 这一行代码。这意味着 `file.user` 是 `None`，无法进行索引操作。
解决方法：在执行 `get_file_by_id(file_id)` 后，确保 `get_file_by_id()` 返回了一个有效的 `File` 对象，并且 `file.user` 不是 `None`。

4. 报错：`KeyError: 'file_id'`
错误原因：这个报错可能出现在 `share_file()` 函数的 `file_id = json_data['file_id']` 这一行代码。这是因为 `json_data` 中没有包含 `file_id` 这个键。
解决方法：在请求的 JSON 数据中，确保包含了一个名为 `file_id` 的键，并提供有效的文件ID值。

5. 报错：`jwt.ExpiredSignatureError: Signature has expired`
错误原因：这个报错出现在 `jwt.decode()` 中，说明JWT令牌已经过期了。
解决方法：检查生成JWT令牌的过期时间设置，确保它与验证JWT令牌时的过期时间设置一致。可以尝试在 `create_access_token()` 中使用 `expires_delta` 参数设置合理的过期时间。

6. 报错：`TypeError: 'NoneType' object is not callable`
错误原因：这个报错可能出现在 `share_download()` 函数的 `share_info = get_share_info(g.user.user_id, share_file_id)` 这一行代码。这意味着 `get_share_info` 是 `None`，但在这里被调用了。
解决方法：确保 `get_share_info()` 返回了一个有效的 `ShareInfo` 对象，可以在 `get_share_info()` 中添加合理的错误处理。


## 三、参考资料
- [JSON Web Token 入门教程- 阮一峰的网络日志](https://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html)
- [Python flask-jwt-extended 4.5.2 documentation](https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage.html)
- [python.ReportClient.ShareInfo - ManageEngine](https://www.manageengine.com/analytics-plus/api/python/python.ReportClient.ShareInfo-class.html)
- [Python JWT 1.3.1 Documentation](https://pyjwt.readthedocs.io/en/stable/)
- [往届师哥师姐的仓库](https://github.com/CreeseWu/AlreadyOnVacation)
