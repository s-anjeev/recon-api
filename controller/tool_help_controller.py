from flask import jsonify
import subprocess
import json  # Import json to handle JSON formatting
from controller.input_validation import is_valid_toolname

class ToolHelpController:
    def __init__(self):
        pass 

    def tool_help_controller(self, toolname):
        vali_toolname = is_valid_toolname(toolname)
        if not vali_toolname:
            return jsonify({"status":"error","message":"invalid tool name."}), 400
        try:
            # Run the tool help command
            command = [toolname, "--help"]
            result = subprocess.run(command, text=True, capture_output=True, check=True)
            
            # Parse and collect the output lines
            list_of_help_lines = result.stdout.strip().split("\n")  # Split lines into a list

            # Optionally, parse the help output into structured JSON if needed
            # Here, we'll simply include all lines in the "help" key for simplicity
            json_output = {"help": list_of_help_lines}
            
            return json.dumps(json_output, indent=4)
        
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing the command: {e}")
            return json.dumps({"error": str(e)}, indent=4)
        
        except FileNotFoundError as e:
            print(f"Tool '{toolname}' not found: {e}")
            return json.dumps({"error": f"Tool '{toolname}' not found"}, indent=4)

