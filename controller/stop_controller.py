from flask import jsonify
from controller import input_validation
import psutil

class StopController:
    def __init__(self):
        pass

    def stop_process(self, process_id):
        self.process_id = process_id

        # Validate the process ID
        if not input_validation.is_valid_process_id(self.process_id):
            return jsonify({"status": "error", "message": "Invalid process ID."}), 400

        try:
            # Attempt to retrieve the process using psutil
            process = psutil.Process(self.process_id)

            # Check if the process is running
            if process.is_running():
                # Attempt to terminate the process
                process.terminate()
                process.wait(timeout=5)  # Wait for the process to terminate (max 5 seconds)
                return jsonify({"status": "success", "message": f"Process with ID {self.process_id} has been stopped."}), 200
            else:
                return jsonify({"status": "error", "message": f"Process with ID {self.process_id} is not running."}), 400

        except psutil.NoSuchProcess:
            return jsonify({"status": "error", "message": f"No process found with ID {self.process_id}."}), 404
        except psutil.AccessDenied:
            return jsonify({"status": "error", "message": f"Access denied: Unable to terminate the process with ID {self.process_id}."}), 403
        except psutil.TimeoutExpired:
            return jsonify({"status": "error", "message": f"Timeout: Process with ID {self.process_id} could not be terminated."}), 408
        except Exception as e:
            return jsonify({"status": "error", "message": f"An unexpected error occurred: {e}"}), 500