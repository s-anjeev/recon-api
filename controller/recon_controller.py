import os
from flask import jsonify
from controller import input_validation
from model.recon_model import TrackOutput
import subprocess
import threading
from datetime import datetime

class ReconController:
    def __init__(self, output_directory="output"):
        # Set the relative output directory (same folder as the project)
        self.output_directory = output_directory

    def recon_controller(self, data):
        try:
            self.tool_name = data["toolname"]
            self.command = data["command"]
            self.filename = data["outputfile"]

            # User input validation and sanitization
            valid_tool_name = input_validation.is_valid_toolname(self.tool_name)
            if not valid_tool_name:
                return jsonify({"status": "error", "message": "Invalid tool name."}), 400

            # Sanitize command input (validation should ensure it's safe)
            sanitized_command = input_validation.sanitize_input(self.command)
            if sanitized_command is None:
                return jsonify({"status": "error", "message": "Invalid command, please check help section."}), 400

            # Sanitize filename and ensure safe directory path
            sanitized_filename = input_validation.sanitize_filename(self.filename)
            if sanitized_filename is None:
                return jsonify({"status": "error", "message": "Invalid file name."}), 400

            # Construct full file path
            full_file_path = self.construct_file_path(sanitized_filename)

            # Execute the command and get the subprocess id
            subprocess_id = self.execute_command(sanitized_command, full_file_path)

            track_output = TrackOutput.save_results(sanitized_command,full_file_path,datetime.now())
            if not track_output:
                return jsonify({
                "status": "success",
                "message": f"Command started. Output will be saved to {full_file_path}",
                "error":"failed to keep track of output file",
                "subprocess_id": subprocess_id
            }), 200

            # Return the subprocess id in response
            return jsonify({
                "status": "success",
                "message": f"Command started. Output will be saved to {full_file_path}",
                "subprocess_id": subprocess_id
            }), 200

        except KeyError as e:
            return jsonify({
                "status": "error",
                "message": "Missing required parameters: 'toolname', 'command', or 'outputfile'."
            }), 400

        except Exception as e:
            print(f"Error: {str(e)}")  # Log the error for better debugging
            return jsonify({
                "status": "error",
                "message": "An unexpected error occurred. Please try again later."
            }), 500

    def construct_file_path(self, sanitized_filename):
        # Ensure the '/output' directory exists in the project folder
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        # Prevent directory traversal by sanitizing the filename further
        sanitized_filename = os.path.basename(sanitized_filename)

        # Construct full path within the 'output' folder
        full_file_path = os.path.join(self.output_directory, sanitized_filename)
        return full_file_path

    def execute_command(self, sanitized_command, full_file_path):
        # Run the tool with arguments provided by users in a non-blocking manner
        try:
            command_list = sanitized_command.split()  # Make sure it's a list of arguments

            # Start the process in the background using Popen
            process = subprocess.Popen(
                command_list,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Get the subprocess ID (pid)
            subprocess_id = process.pid

            # Function to write output to the file
            def write_output_to_file():
                with open(full_file_path, "w") as file:
                    for line in process.stdout:
                        file.write(line)  # Write each line of the command's output

                # After the process finishes, check for any error
                stderr_output = process.stderr.read()
                if stderr_output:
                    print(f"Error Output: {stderr_output.decode()}")

            # Run the output saving in a separate thread to allow non-blocking execution
            threading.Thread(target=write_output_to_file).start()

            # Return the subprocess ID immediately
            return subprocess_id

        except Exception as e:
            print(f"Unexpected error: {e}")
            raise Exception("An unexpected error occurred while executing the command.")
