from flask import jsonify
from controller import input_validation
import psutil


class StatusController:
    def __init__(self):
        pass

    def status_controller(self,process_id):
        self.processs_id = process_id

        if not input_validation.is_valid_process_id(self.processs_id):
            return jsonify({"status":"error","message":"invalid recon_id"}), 400
        
        try:
            # Attempt to retrieve the process details using psutil
            process = psutil.Process(self.processs_id)

            # Check if the process is running and retrieve its status
            if process.is_running():
                status = process.status()
                return jsonify({"status":"success","message":f"Process with self.processs_id {self.processs_id} is currently {status}."}), 400
            else:
                return jsonify({"status":"success","message":f"Process with self.processs_id {self.processs_id} is not running."}), 400
        except psutil.NoSuchProcess:
            return jsonify({"status":"success","message":f"No process found with self.processs_id {self.processs_id}."}), 400
        except psutil.AccessDenied:
            return jsonify({"status":"success","message":f"Access denied: Unable to check the status of the process with self.processs_id {self.processs_id}."}), 400
        except Exception as e:
            return jsonify({"status":"success","message":f"An unexpected error occurred: {e}"}), 400



