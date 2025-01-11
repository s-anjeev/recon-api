from flask import Flask, jsonify
from flask_cors import CORS
import logging
from flask_talisman import Talisman
from utils.limiter import limiter
from routes.home import home_bp
from routes.login import login_bp, logout_bp
from routes.recon import full_recon_bp, recon_bp
from routes.result import result_bp
from routes.status import status_bp
from routes.stop import stop_bp
from routes.all_tools import getall_bp
from routes.tool import tool_bp
from routes.tool_help import tool_help_bp

app = Flask(__name__)

# Initialize Flask-Talisman
talisman = Talisman(app, force_https=False)

# Define your CSP policy
csp = {
    'default-src': "'self'",  # Only allow content from the same origin
    'script-src': "'self' https://cdn.jsdelivr.net",  # Allow scripts from the same origin and CDN
    'style-src': "'self' 'unsafe-inline'",  # Allow styles from the same origin and inline styles
    'img-src': "'self' data:",  # Allow images from the same origin and inline data URIs
    'font-src': "'self' https://fonts.googleapis.com",  # Allow fonts from Google Fonts
    'connect-src': "'self'",  # Restrict AJAX requests to the same origin
    'frame-src': "'none'",  # Prevent embedding of your site in an iframe
    'object-src': "'none'",  # Disable plugin-based content (Flash, etc.)
}

# Apply the CSP policy
talisman.content_security_policy = csp


CORS(app, resources={
    r"/*": {
        "origins": ["https://example1.com", "https://example2.com"],
        "methods": ["OPTIONS", "GET", "POST", "PATCH", "PUT"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
},supports_credentials=True)


# initialize logging
logging.basicConfig(level=logging.INFO)


# Regester blueprint
app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(full_recon_bp)
app.register_blueprint(recon_bp)
app.register_blueprint(result_bp)
app.register_blueprint(status_bp)
app.register_blueprint(stop_bp)
app.register_blueprint(getall_bp)
app.register_blueprint(tool_bp)
app.register_blueprint(tool_help_bp)


# initialize limiter with the app
limiter.init_app(app)

# Global error handler for 400 Bad Request
@app.errorhandler(400)
def handle_400_error(e):
    return jsonify({"Status":"Error","Message": "Bad Request"}), 400

# Global error handler for 403 Forbidden
@app.errorhandler(403)
def handle_403_error(e):
    return jsonify({"Status":"Error","Message": "Forbidden"}), 403

# Global error handler for 404 Forbidden
@app.errorhandler(404)
def handle_404_error(e):
    return jsonify({"Status":"Error","Message": "Not Found"}), 404

# Global error handler for 405 Method Not Allowed
@app.errorhandler(405)
def handle_405_error(e):
    return jsonify({"Status":"Error","Message": "Method Not Allowed"}), 405

# Global error handler for 408 Request Timeout
@app.errorhandler(408)
def handle_408_error(e):
    return jsonify({"Status":"Error","Message": "Request Timeout"}), 408

# Global error handler for 413 Payload Too Large
@app.errorhandler(413)
def handle_413_error(e):
    return jsonify({"Status":"Error","Message": "Payload Too Large"}), 413

# Global error handler for 415 Unsupported Media Type
@app.errorhandler(415)
def handle_415_error(e):
    return jsonify({"Status":"Error","Message": "Unsupported Media Type"}), 415

# Global error handler for 418 I'm a teapot (for fun or custom responses)
@app.errorhandler(418)
def handle_418_error(e):
    return jsonify({"Status":"Error","Message": "Error"}), 418

# Global error handler for 429 
@app.errorhandler(429)
def handle_429_error(e):
    return jsonify({
        "Status": "Error",
        "Message": "Too Many Requests"
    }), 429

# Global error handler for 502 Bad Gateway
@app.errorhandler(502)
def handle_502_error(e):
    return jsonify({"Status":"Error","Message": "Bad Gateway"}), 502

# Global error handler for 503 Service Unavailable
@app.errorhandler(503)
def handle_503_error(e):
    return jsonify({"Status":"Error","Message": "Service Unavailable"}), 503


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host="127.0.0.1", port=5000)


