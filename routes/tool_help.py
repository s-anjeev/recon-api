from flask import Blueprint, jsonify, request
# from utils.limiter import limiter  # Import the limiter from extensions.py
from utils.user_authentication import authentication_required
from controller.tool_help_controller import ToolHelpController

tool_help_bp = Blueprint('tool help', __name__)

# apply rate limit to specific Blueprint routes 
@tool_help_bp.route('/api/recon/<toolname>/help', methods=["GET"])
@authentication_required
# @limiter.limit('10 per minute')
def tool_help(toolname):
    try:
        tool_controller = ToolHelpController()
        help_json = tool_controller.tool_help_controller(toolname)
        return help_json
        
    except Exception as e:
        print(f"error: {e}")
        return jsonify({'message': 'missing or invalid Authorization header.','status':'Error'}), 401