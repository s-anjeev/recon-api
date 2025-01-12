from flask import Blueprint, jsonify
# from utils.limiter import limiter
from controller.results_controller import FileReader, FileLister

# creating the result blueprint 
result_bp = Blueprint('result',__name__)

# apply rate limit to specific Blueprint routes
@result_bp.route('/api/recon/results/<output_file>', methods=["GET"])
# @limiter.limit('10 per minute')
def get_results(output_file):
    try:
        reader = FileReader(output_directory="output")  # Specify the output folder
        content = reader.read_file(output_file, chunk_size=1024)  # Adjust chunk_size as needed
        return content

    except Exception as e:
        print(f"error: {e}")
        return jsonify({'message': 'missing or invalid Authorization header.','status':'Error'}), 401
    


# getting all results at once
all_result_bp = Blueprint('all result',__name__)

# apply rate limit to specific Blueprint routes
@all_result_bp.route('/api/recon/results/all', methods=["GET"])
# @limiter.limit('10 per minute')
def get_all_results():
    try:
        lister = FileLister(output_directory="output")  # Specify the output directory if needed
        files_json = lister.list_files()
        return files_json
        
    except Exception as e:
        print(f"error: {e}")
        return jsonify({'message': 'missing or invalid Authorization header.','status':'Error'}), 401