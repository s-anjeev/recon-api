import subprocess
import json  # Import json to handle JSON formatting

class AllTollsController:
    def __init__(self):
        pass 

    def all_tools_controller(self):
        try:
            # Get the username in the /home directory
            cmd = ["ls", "/home"]
            user_result = subprocess.run(cmd, text=True, capture_output=True, check=True)
            user = user_result.stdout.strip()  # Extract username and remove extra spaces/newlines
            
            # Add username into the path dynamically
            path = f"/home/{user}/tools"
            command = ["ls", path]  # Example: List files in the tools directory

            # Execute the command to list the tools
            result = subprocess.run(command, text=True, capture_output=True, check=True)
            
            # Parse and collect the list of tools from the output
            list_of_tools = result.stdout.strip().split("\n")  # Split lines into a list
            
            # Create a JSON-formatted output
            json_output = {"tools": list_of_tools}
            return json.dumps(json_output, indent=4)
        
        except subprocess.CalledProcessError as e:
            print("An error occurred while executing the command.")
            print(e)
