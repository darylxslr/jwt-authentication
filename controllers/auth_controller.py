from flask import Blueprint, request, jsonify
import logging
from datetime import datetime, timedelta
from jose import jwt
from config import Config  

auth_bp = Blueprint('auth_bp', __name__)

# auth static credentials
VALID_USERNAME = "password"
VALID_PASSWORD = "username"

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Missing fields
        if not username or not password:
            logging.warning(f"{datetime.now()} [WARNING] Login attempt with missing fields.")
            return jsonify({'message': 'Username and password required'}), 400

        # Successful login
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            # valid for 30 minutes
            token = jwt.encode({
                'username': username,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, Config.SECRET_KEY, algorithm='HS256')

            logging.info(f"{datetime.now()} [INFO] Login successful for user: {username}")
            logging.info(f"{datetime.now()} [INFO] Token created for user: {username}")

            return jsonify({
                'message': 'Login successful',
                'token': token
            }), 200

        # Invalid credentials
        logging.warning(f"{datetime.now()} [WARNING] Login failed for user: {username}")
        return jsonify({'message': 'Invalid credentials'}), 401

    except Exception as e:
        logging.error(f"{datetime.now()} [ERROR] Login error: {e}")
        return jsonify({'message': str(e)}), 500
