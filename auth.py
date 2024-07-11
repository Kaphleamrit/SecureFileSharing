from flask import jsonify, request
import jwt
import datetime
from functools import wraps

users = {}  # In-memory user store, replace with a database in production
roles = {}  # In-memory roles store

def register_user(username, password):
    if username in users:
        return jsonify({"message": "User already exists"}), 400
    users[username] = password  # Hash passwords in a real application
    roles[username] = 'admin'  # Assign default role as 'admin'; adjust as needed
    return jsonify({"message": "User registered successfully"}), 201

def login_user(username, password):
    if users.get(username) != password:
        return jsonify({"message": "Invalid credentials"}), 401
    token = jwt.encode({
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, 'your_secret_key')
    return jsonify({'token': token})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, 'your_secret_key', algorithms=["HS256"])
            current_user = data['user']
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated
