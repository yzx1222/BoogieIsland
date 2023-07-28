# auth/views.py
from flask import render_template, redirect, request, url_for, jsonify
import json
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from app.auth.forms import SignUpForm
from app.auth.forms import SignInForm
from app.user.user import User
from app.extensions import db
from app.blueprints import auth
from app.extensions import login_manager

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.json

    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')
    username=data.get('username')
    print(username)
    # 检查密码是否匹配
    if password != confirm_password:
        return jsonify({'error': '密码不匹配'}), 400

    # 检查邮箱是否已被注册
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': '邮箱已被注册'}), 400
    
    User.create_new_user(email,password,username)
    return jsonify({'message': '注册成功！'}), 200 # 额外的用户信息

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first_or_404()
    user_data = {
    'id': user.id,
    'email': user.email,
    'name': user.name,
    }
    if user.is_correct_password(password):
        login_user(user)
        return jsonify({'message': '登录成功！','user': json.dumps(user_data)}), 200 # 额外的用户信息
    else:
        return jsonify({'error': '登录失败，用户名或密码错误'}), 401
        

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': '成功注销！'}), 200

@auth.route('/user', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({'username': current_user.username}), 200
    else:
        return jsonify({'message': '未登录'}), 401

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
