from jwt.exceptions import ExpiredSignatureError, InvalidTokenError  # Correct imports
from flask import request,jsonify
import jwt
# from config.config import jwt_secret

jwt_secret={
    "secret":"asfv6s4g65fg1bfxvsk62ih4bf33846fih3rijebrgdfg5b4f2g1b6f5g4bf591b"
}


def authentication_required(func):
    def wrapper(*args, **kwargs):
        secret = jwt_secret["secret"]

        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Missing or invalid Authorization header.', 'status': 'error'}), 401
        
        token = auth_header.split(' ')[1].strip()

        try:
            decode = jwt.decode(token, secret, algorithms=["HS256"])  # Use list for algorithms
            if decode.get("role") != "admin":  # Use get() to handle missing keys
                return jsonify({'message': 'Access forbidden.', 'status': 'error'}), 403
            
            return func(*args, **kwargs)

        except ExpiredSignatureError:
            return jsonify({'message': 'Token has expired.', 'status': 'error'}), 401

        except InvalidTokenError:
            return jsonify({'message': 'Invalid token.', 'status': 'error'}), 401

        except Exception as e:
            print("Unexpected error:", e)
            return jsonify({'message': 'An unexpected error occurred.', 'status': 'error'}), 500

    return wrapper