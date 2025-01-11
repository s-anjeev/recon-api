from flask import Blueprint, jsonify, request
from utils.limiter import limiter  # Import the limiter from extensions.py
from utils.user_authentication import authentication_required
from controller.all_tools_controller import AllTollsController


getall_bp = Blueprint('get all tools', __name__)

# apply rate limit to specific Blueprint routes 
@getall_bp.route('/api/recon/get_all_tools', methods=["GET"])
@authentication_required
@limiter.limit('10 per minute')
def all_tools():
    try:
        # get the authorization header
        auth_header = request.headers.get('Authorization')

        # check if the authorization header is present and correctly formatted
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'Error': 'Missing or invalid Authorization header.','Status':'Error'}), 401
        
        token = auth_header.split(' ')[1].strip() # extracting the token

        controller_object = AllTollsController()
        return controller_object.all_tools_controller()
        
    except Exception as e:
        print(f"error: {e}")
        return jsonify({'message': 'missing or invalid Authorization header.','status':'Error'}), 401