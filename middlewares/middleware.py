from functools import wraps
from flask import request, jsonify
from controllers.auth.AuthController import AuthController
from util.debug import debug
def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            
            if not token:
                return jsonify({"message": "Token is missing"}), 401

            if token.startswith('Bearer '):
                token = token.split(" ")[1] 
                
            payload = AuthController.verify_token(token)

            if not payload:
                return jsonify({"message": "Invalid or expired token"}), 401

            if payload['role'] not in roles:
                return jsonify({"message": "Unauthorized access"}), 403

            # Add user info to request context
            request.user_id = payload['user_id']
            request.role = payload['role']
            debug(f"user id {request.user_id} user role: {request.role} ")
            return f(*args, **kwargs)
        return decorated_function
    return decorator