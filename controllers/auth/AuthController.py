# /backend/repo/project/backend/controllers/auth/AuthController.py

import jwt
import datetime
from flask import request, jsonify
from util.debug import debug
from db.base import get_db_connection

SECRET_KEY = 'your_secret_key'

class AuthController:

    @staticmethod
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check for valid email and password (Assuming a basic check here)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            token = AuthController.generate_token(user)
            response_data = {
                'message': 'Login successful',
                'token': token,
                'user_role': user[5],  # Assuming user[5] is the role
                'name': user[1],  # Assuming user[1] is the name
                'success': True,
            }
            return jsonify(response_data)
        else:
            response_data = {
                'message': 'Invalid credentials',
                'success': False
            }
            return jsonify(response_data), 401

    @staticmethod
    def generate_token(user):
        payload = {
            'user_id': user[0],  # Assuming user[0] is the user ID
            'role': user[5],  # Assuming user[5] is the role
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration in 1 hour
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
