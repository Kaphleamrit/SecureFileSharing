
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_file(file_data):
    return cipher_suite.encrypt(file_data)

def decrypt_file(encrypted_data):
    return cipher_suite.decrypt(encrypted_data)


from flask import Flask, request, render_template, redirect, url_for, session, jsonify, send_file
from auth import register_user, login_user, token_required, roles
from access_control import check_permission
from file_transfer import sftp_upload_file
import os
import io
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response, status = register_user(username, password)
        if status == 201:
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error=response.json['message'])
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response, status = login_user(username, password)
        if status == 200:
            session['token'] = response.json['token']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error=response.json['message'])
    return render_template('login.html')

@app.route('/home')
@token_required
def home(current_user):
    return render_template('home.html', user=current_user)

@app.route('/upload', methods=['GET', 'POST'])
@token_required
def upload_file(current_user):
    if request.method == 'POST':
        file = request.files['file']
        encrypted_file = encrypt_file(file.read())
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename + '.enc')
        with open(file_path, 'wb') as f:
            f.write(encrypted_file)
        return jsonify({'message': 'File uploaded successfully'})
    return render_template('upload.html')

@app.route('/download', methods=['GET', 'POST'])
@token_required
def download_file(current_user):
    if request.method == 'POST':
        file_name = request.form['file_name']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name + '.enc')
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

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
