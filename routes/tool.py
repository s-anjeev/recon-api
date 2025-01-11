# this endpoint will allow an user to add or remove tools
# operation : add or remove this parameter will decide operation that current request will perform
# languge : python, go, bash programming language in which tool in written
# repolink : link link of github repo


from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from utils.limiter import limiter
# from controller.tool_controller import ToolController

# create the blueprint
tool_bp = Blueprint('tool',__name__)

@tool_bp.route('/api/tool', methods=["POST"])
@limiter.limit("5 per 5 minutes")
def tool():

    try:
        data = request.get_json(force=True) # Ensure JSON parsing even if content-type isn't set correctly

        # check if data is missing or empty
        if not data:
            return jsonify({
                "status":"error",
                "message": "Request body cannot be empty. Please provide valid JSON."
            }), 400
        
        # passing commands to controller for further processing
        # tool_controller = ToolController()
        # return tool_controller.tool_controller(data)
        return "under development"
    
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