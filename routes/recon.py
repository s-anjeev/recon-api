from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest
from utils.limiter import limiter
from utils.user_authentication import authentication_required
from controller.recon_controller import ReconController

# create the blueprint for full recon
full_recon_bp = Blueprint('fullrecon', __name__)

# apply rate limit to specific Blueprint routes
@full_recon_bp.route('/api/recon/start', methods=["POST"])
@authentication_required
@limiter.limit("5 per minute")
def full_recon():
    # get the authorization header
    auth_header = request.headers.get('Authorization')

    # check if the authorization header is present and correctly formatted
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'Error': 'Missing or invalid Authorization header.','Status':'Error'}), 401
    
    token = auth_header.split(' ')[1].strip() # Extracting the token
    
    # check if user is authorized or not.
    authorized = True

    if authorized:
        # attempt to parse JSON data from the request body
        try:
            data = request.get_json(force=True) # Ensure JSON parsing even if content-type is not set correctly

            # check if data is missing or empty
            if not data:
                return jsonify({
                "Status":"Error",
                "Error": "Invalid data",
                "Message": "Request body cannot be empty. Please provide valid JSON."
            }), 400

            return "data is being processed."
        except BadRequest:
            # specific error for invalid JSON structure or invalid content type
            return jsonify({
            "Status":"Error",
            "Error": "Invalid JSON",
            "Message": "Request body must be valid JSON."
        }), 400

        except Exception as e:
            # catch unecpected errors and provide a generic server error message
            # log the error internally (use app.logger for this)
            return jsonify({
            "Status":"Error",
            "Error": "Server Error",
            "Message": "An unexpected error occurred. Please try again later."
        }), 500
    else:
        return jsonify({'Error': 'Unauthorized please login.','Status':'Error'}), 401
    



# this toll will run a specific tool based on parameters given by us
# parameters
# name name of the tool
# command command to be executed

# create the blueprint for recon
recon_bp = Blueprint('recon', __name__)

# apply rate limit to specific Blueprint routes
@recon_bp.route('/api/recon/tool', methods=["POST"])
@authentication_required
@limiter.limit("5 per minute")
def recon():
    try:
        data = request.get_json(force=True) # Ensure JSON parsing even if content-type isn't set correctly

        # check if data is missing or empty
        if not data:
            return jsonify({
                "status":"error",
                "message": "Request body cannot be empty. Please provide valid JSON."
            }), 400
        
        recon_obj = ReconController()
        return recon_obj.recon_controller(data)
    
    except BadRequest:
        # Specific error for invalid JSON structure or invalid content type
        return jsonify({
            "status":"error",
            "message": "Request body must be valid JSON."
        }), 400
    
    except Exception as e:
        print(f"error: {e}")
        return jsonify({
            "status":"error",
            "message": "An unexpected error occurred. Please try again later."
        }), 500