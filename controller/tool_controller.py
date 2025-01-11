# this controller will receive commands from tool route and add (install) or remove (uninstall) tool.
from flask import jsonify


class ToolController:
    def __init__(self):
        pass

    def tool_controller(self,data):
        
        try:
            operation = data["operation"]
            name = data["name"]
            language = data["language"]
            gitrepo = data["repolink"]

            commands_to_execute = self.command_composition(language,gitrepo,operation,name)
            return commands_to_execute
        
        except KeyError as e:
            print("Error: key error")
            return jsonify({
                "status":"error",
                "message":"key error"
            }), 400
        
        except Exception as e:
            print(f"Error: {str(e)}")
            jsonify({
                "Status": "Error",
                "Error": "Server Error",
                "Message": "An unexpected error occurred. Please try again later."
            }), 500

    def command_composition(self,language,gitrepo,operation,name):
        operations = ["add","remove"]
        languages = ["python","go","bash","c","c++","javascript","ruby","php","Perl"]

        if operation not in operations:
            return jsonify({"ststus":"error","message":"invalid operation"}), 400
        if language not in languages:
            return jsonify({"ststus":"error","message":"language not supported"}), 400
        
        if operation == "add" and language == "python":
            command = f"git clone {gitrepo}"
            return command
        
        elif operation == "add" and language == "go":
            command = f"go install -v {gitrepo}"
            return command
        
        elif operation == "add" and language == "bash":
            command = f"git clone {gitrepo}"
            return command
        else:
            return jsonify({"ststus":"error","message":"somthing went wrong."}), 400