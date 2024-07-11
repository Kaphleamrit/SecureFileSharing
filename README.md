
# Secure File Sharing Platform

A secure file-sharing platform with encryption and access control mechanisms to ensure data integrity and confidentiality during file transfer.

## Features

- **User Authentication**: Register and login users with JWT-based authentication.
- **File Encryption**: Encrypt files before uploading to ensure confidentiality.
- **Access Control**: Role-based access control to restrict who can upload and download files.
- **File Integrity**: Ensure the integrity of files using encryption.
- **Secure Transfer**: Use HTTPS for secure communication and SFTP for file transfers.

## Tech Stack

- **Backend**: Python, Flask
- **Security**: JWT, Cryptography
- **Frontend**: HTML, CSS, Bootstrap
- **File Transfer**: Paramiko (SFTP)

## Project Structure

```
secure_file_transfer/
│
├── __init__.py
├── app.py
├── auth.py
├── encryption.py
├── file_transfer.py
├── access_control.py
├── requirements.txt
├── static/
│   ├── css/
│   │   └── style.css
└── templates/
    ├── base.html
    ├── login.html
    ├── register.html
    ├── upload.html
    └── download.html
```

## Getting Started

### Prerequisites

- Python 3.x
- pip (Python package installer)
- OpenSSL (for generating SSL certificates)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/secure-file-transfer.git
   cd secure-file-transfer
   ```

2. **Set up a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Generate SSL certificates**:

   ```bash
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
   ```

### Running the Application

1. **Run the Flask application**:

   ```bash
   python -m secure_file_transfer.app
   ```

2. **Access the application**:

   Open your browser and navigate to `https://127.0.0.1:5000`

## Usage

### Register

- Go to `/register`
- Fill out the registration form and submit

### Login

- Go to `/login`
- Fill out the login form and submit
- The token will be saved in `localStorage`

### Upload Files

- Go to `/upload`
- Choose a file and submit
- The token will be included in the request headers

### Download Files

- Go to `/download`
- Enter the file name (without the `.enc` extension) and submit
- The token will be included in the request headers
- If the file exists, it will be downloaded

## Security Features

- **JWT Authentication**: Secure user authentication with JSON Web Tokens.
- **File Encryption**: Encrypt files before storing them on the server.
- **Role-Based Access Control**: Different access levels for admins and regular users.
- **HTTPS**: Secure communication using HTTPS.
- **SFTP**: Secure file transfer using SFTP.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Cryptography](https://cryptography.io/)
- [Paramiko](https://www.paramiko.org/)
