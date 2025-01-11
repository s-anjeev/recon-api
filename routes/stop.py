from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest
from utils.limiter import limiter  # Import the limiter from extensions.py
from controller.stop_controller import StopController

stop_bp = Blueprint('stop', __name__)

# apply rate limit to specific Blueprint routes 
@stop_bp.route('/api/recon/stop/<recon_id>', methods=["GET"])
@limiter.limit('10 per minute')
def stop(recon_id):
    try:
        stop_controller_obj = StopController()
        return stop_controller_obj.stop_process(recon_id)
        
    except Exception as e:
        print(f"error: {e}")
        return jsonify({'message': 'missing or invalid Authorization header.','status':'Error'}), 401