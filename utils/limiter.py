# from flask import Flask, request
# from flask_socketio import SocketIO, emit
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# from redis import Redis
# from flask_limiter.util.redis import RedisStorage

# # Initialize Flask app
# app = Flask(__name__)

# # Initialize Redis connection
# redis_client = Redis.from_url('redis://localhost:6379/0')  # Adjust the Redis URL if needed

# # Initialize Limiter with RedisStorage for rate limiting
# limiter = Limiter(
#     key_func=get_remote_address,
#     default_limits=["200 per day", "50 per hour"],  # Global limits
#     storage=RedisStorage(redis_client)  # Use Redis for rate limiting storage
# )