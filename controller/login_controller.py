from flask import jsonify
from controller import input_validation
from utils import hash
import jwt
from config.config import jwt_secret
from datetime import datetime,timedelta
from model import login_model

class LoginController:
    def __init__(self):
        self.login_model = login_model.LoginModel()
        pass

    def login_controller(self, data):
        try:
            self.email = data["email"]
            self.password = data["password"]

        #     # Uncomment and implement validation
        #     # email validation
            mail = input_validation.email_validation(self.email)
            if not mail:
                return jsonify({"status":"error","message":"invalid username or password"}), 401

            # password validation
            password = input_validation.password_validation(self.password)  # Assuming password validation exists
            if not password:
                return jsonify({"status":"error","message":"invalid username or password"}), 401
            
            password_hash = hash.password_hash(self.password)

            # # Check user credentials
            user_status = self.login_model.user_login(self.email, password_hash)
            if not user_status:
                return jsonify({"status": "error", "message": "invalid username or password"}), 401
            
            # calculating jwt expiry time
            exp_time = datetime.now() + timedelta(minutes=60)
            # convert into epoc time
            exp_time = int(exp_time.timestamp())
            
            # adding expiry time to
            user_status['exp'] = exp_time

            # generating jwt for authenticated user
            secret = jwt_secret['secret']
            try:
                token = jwt.encode(user_status, secret,algorithm="HS256")
                
                # keeping track of user session
                if token:
                    self.login_model.user_status(user_status['user_id'])
                    return jsonify({"status": "success", "message": "Login successful", "jwt": token}), 200
                
            except Exception as e:
                print(f"error: {e}")
                return jsonify({
            "status":"error",
            "message": "An unexpected error occurred. Please try again later."
        }), 500 
        

        except KeyError as e:
            # Handle the case where the 'mail' or 'password' is missing
            return jsonify({
                "status":"error",
                "message":"invalid username or password"
            }), 400
        
        except Exception as e:
            print(f"Error: {str(e)}")  # Log the error for better debugging
            return jsonify({
                "Status": "Error",
                "Error": "Server Error",
                "Message": "An unexpected error occurred. Please try again later."
            }), 500
