import os
import os
import json  # For JSON conversion


class FileReader:
    def __init__(self, output_directory="output"):
        self.output_directory = output_directory

    def read_file(self, file_name, chunk_size=1024):
        try:
            # Construct the full file path
            file_path = os.path.join(self.output_directory, os.path.basename(file_name))

            # Check if the file exists
            if not os.path.exists(file_path):
                print(f"Error: File '{file_name}' not found in '{self.output_directory}' directory.")
                return None

            # Open the file in read mode
            file_content = ""
            with open(file_path, "r") as file:
                print(f"Reading file: {file_name}")

                # Read and process the file in chunks
                while True:
                    chunk = file.read(chunk_size)  # Read chunk_size bytes
                    if not chunk:  # If no more data, break the loop
                        break
                    file_content += chunk  # Append the chunk to the content string

                print("\nFile reading completed.")
            return file_content
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None



class FileLister:
    def __init__(self, output_directory="output"):
        self.output_directory = output_directory

    def list_files(self):
        try:
            # Check if the directory exists
            if not os.path.exists(self.output_directory):
                return json.dumps({
                    "status": "error",
                    "message": f"Directory '{self.output_directory}' does not exist.",
                    "files": []
                })

            # List all files in the directory
            files = [
                file
                for file in os.listdir(self.output_directory)
                if os.path.isfile(os.path.join(self.output_directory, file))
            ]

            # Return the list of files in JSON format
            return json.dumps({
                "status": "success",
                "message": f"Files listed from directory '{self.output_directory}'.",
                "files": files
            }, indent=4)
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"An error occurred: {e}",
                "files": []
            }, indent=4)