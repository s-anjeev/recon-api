import re

def is_valid_process_id(process_id):
     # Regular expression to check if the input is a positive whole number
    pattern = r'^[1-9]\d*$'
    return bool(re.match(pattern, process_id))

def is_valid_toolname(toolname):
    # Define the regex pattern to allow letters, numbers, underscores, and hyphens
    pattern = r'^[a-zA-Z0-9_-]+$'
    
    # Check if the toolname matches the pattern
    if re.match(pattern, toolname):
        return True
    else:
        return False

def sanitize_input(command):
    # Ensure the command is safe, for example, no shell metacharacters
    if re.search(r"[;&|><`$!(){}\\]", command):
        return None  # Invalid command due to dangerous characters
    return command

def sanitize_filename(filename):
    # Allow only alphanumeric characters, underscores, and dots
    if re.match(r'^[a-zA-Z0-9_.]+$', filename):
        return filename
    return None  # Invalid filename due to unsafe characters


# function for validating email
def email_validation(email):        
    if not email:
        return False
    
    # Regular expression for validating an email
    pattern = re.compile(
    r'^(?P<local_part>[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+)@(?P<domain>(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})$'
    )
    is_valid_email =  bool(pattern.match(email))
    if is_valid_email == True:
        return True
    else:
        return False


# Function for validatig password
def password_validation(password):
        password = str(password)
        
        if not password:
            return False
        
        if len(password) < 8:
            return False
        
        if len(password) > 36:
            return False
        
        return True

