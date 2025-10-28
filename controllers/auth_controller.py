from flask import Blueprint, request, jsonify
import logging
from datetime import datetime

auth_bp = Blueprint('auth_bp', __name__)

# static auth
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
            logging.info(f"{datetime.now()} [INFO] Login successful for user: {username}")
            return jsonify({'message': 'Login successful'}), 200
        else:
            logging.warning(f"{datetime.now()} [WARNING] Login failed for user: {username}")
            return jsonify({'message': 'Invalid credentials'}), 401

    except Exception as e:
        logging.error(f"{datetime.now()} [ERROR] Login error: {e}")
        return jsonify({'message': str(e)}), 500
