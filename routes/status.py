from flask import Blueprint, jsonify
from utils.limiter import limiter
from controller.status_controller import StatusController


# creating the result blueprint 
status_bp = Blueprint('satus',__name__)

# apply rate limit to specific Blueprint routes 
@status_bp.route('/api/recon/status/<recon_id>', methods=["GET"])
@limiter.limit('10 per minute')
def get_status(recon_id):
    try:
        status_controller_obj = StatusController()
        return status_controller_obj.status_controller(recon_id)
        
    except Exception as e:
        print(f"error: {e}")
        return jsonify({'message': 'missing or invalid Authorization header.','status':'Error'}), 401