from flask import jsonify
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError  # Correct imports
from config.config import jwt_secret
from model.logout_model import LogoutModel
 

class LogoutController:
    def __init__(self):
        self.logout_model = LogoutModel()
        pass

    def logout_user(self, jwt_token):
        try:
            # Decoding JWT
            secret = jwt_secret['secret']
            user_details = jwt.decode(jwt_token, secret, algorithms=["HS256"])  # Use 'algorithms' (plural)

            # Perform logout operation
            result = self.logout_model.logout_model(user_details['user_id'])
            if result:
                return jsonify({'message': 'You have successfully logged out.', 'status': 'success'}), 200
            else:
                return jsonify({'message': 'Logout failed.', 'status': 'error'}), 500  # Handle unexpected failures
            # return "ffff"

        except ExpiredSignatureError:
            print("Error: Token has expired.")
            return jsonify({'message': 'Token has expired.', 'status': 'error'}), 401

        except InvalidTokenError:
            print("Error: Invalid token.")
            return jsonify({'message': 'Invalid token.', 'status': 'error'}), 401

        except Exception as e:
            print("Unexpected error:", e)
            return jsonify({'message': 'An unexpected error occurred.', 'status': 'error'}), 500
