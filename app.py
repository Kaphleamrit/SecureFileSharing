from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
from auth import users, register_user, login_user, token_required, roles
from access_control import check_permission
from file_transfer import sftp_upload_file
from cryptography.fernet import Fernet
import os
import io

# Generate a key for encryption and decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_file(file_data):
    return cipher_suite.encrypt(file_data)

def decrypt_file(encrypted_data):
    return cipher_suite.decrypt(encrypted_data)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return register_user(username, password)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return login_user(username, password)
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
@token_required
def upload_file(current_user):
    role = roles.get(current_user)  # Retrieve user role from in-memory store
    if not check_permission(role, 'upload'):
        return jsonify({'message': 'Permission denied'}), 403
    if request.method == 'POST':
        file = request.files['file']
        encrypted_file = encrypt_file(file.read())
        file_path = os.path.join(UPLOAD_FOLDER, file.filename + '.enc')
        with open(file_path, 'wb') as f:
            f.write(encrypted_file)
        return jsonify({'message': 'File uploaded successfully'})
    return render_template('upload.html')

@app.route('/download', methods=['GET', 'POST'])
@token_required
def download_file(current_user):
    role = roles.get(current_user)  # Retrieve user role from in-memory store
    if not check_permission(role, 'download'):
        return jsonify({'message': 'Permission denied'}), 403
    if request.method == 'POST':
        file_name = request.form['file_name']
        file_path = os.path.join(UPLOAD_FOLDER, file_name + '.enc')
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                decrypted_file = decrypt_file(f.read())
            return send_file(
                io.BytesIO(decrypted_file),
                mimetype='application/octet-stream',
                as_attachment=True,
                download_name=file_name
            )
        else:
            return jsonify({'message': 'File not found'}), 404
    return render_template('download.html')

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
