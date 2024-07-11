from flask import jsonify, session, redirect, url_for
import jwt
import datetime
from functools import wraps

users = {}
roles = {}

def register_user(username, password):
    if username in users:
        return jsonify({"message": "User already exists"}), 400
    users[username] = password
    roles[username] = 'admin'
    return jsonify({"message": "User registered successfully"}), 201

def login_user(username, password):
    if users.get(username) != password:
        return jsonify({"message": "Invalid credentials"}), 401
    token = jwt.encode({
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, 'your_secret_key')
    return jsonify({'token': token}), 200

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('token')
        if not token:
            return redirect(url_for('login'))
        try:
            data = jwt.decode(token, 'your_secret_key', algorithms=["HS256"])
            current_user = data['user']
        except:
            return redirect(url_for('login'))
        return f(current_user, *args, **kwargs)
    return decorated
