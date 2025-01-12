from flask import Blueprint, jsonify
# from utils.limiter import limiter

# create the home Blueprint
home_bp = Blueprint('home',__name__)

@home_bp.route('/', methods=["GET"])
# @limiter.limit("10 per minute")  # Custom limit for this route
def home():
    return jsonify({"Status":"Success","Message":"Wellcome to the home page."})