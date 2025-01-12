from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest
from controller.login_controller import LoginController
from controller.logout_controller import    LogoutController
# from utils.limiter import limiter  # Import the limiter from extensions.py
from utils.user_authentication import authentication_required


# Create the login Blueprint
login_bp = Blueprint('login', __name__)

# Apply rate limiting to specific Blueprint routes
@login_bp.route('/login', methods=["POST"])
# @limiter.limit("5 per 5 minutes")
def login():
    # Attempt to parse JSON data from the request body
    try:
        data = request.get_json(force=True)  # Ensure JSON parsing even if content-type isn't set correctly
        
        # Check if data is missing or empty
        if not data:
            return jsonify({
                "status":"error",
                "message": "Request body cannot be empty. Please provide valid JSON."
            }), 400

        # Pass the data to the login logic
        login_controller = LoginController()
        return login_controller.login_controller(data)
    
    except BadRequest:
        # Specific error for invalid JSON structure or invalid content type
        return jsonify({
            "status":"error",
            "message": "Request body must be valid JSON."
        }), 400

    except Exception as e:
        # Catch unexpected errors and provide a generic server error message
        # Log the error internally (you can use app.logger for this)
        print(f"error: {e}")
        return jsonify({
            "status":"error",
            "message": "An unexpected error occurred. Please try again later."
        }), 500



# log out
# Create the logout Blueprint
logout_bp = Blueprint('logout', __name__)

# Apply rate limiting to specific Blueprint routes
@logout_bp.route('/logout', methods=["GET"])
# @limiter.limit("5 per 5 minutes")
@authentication_required
def logout():
    try:
 
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')

        # Check if the Authorization header is present and correctly formatted
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'missing or invalid Authorization header.','status':'Error'}), 401
        
        token = auth_header.split(' ')[1].strip()  # Extract the token

        logout_controller = LogoutController()
        return logout_controller.logout_user(token)

    except Exception as e:
        print(f"error: {e}")
        return jsonify({'message': 'missing or invalid Authorization header.','status':'Error'}), 401