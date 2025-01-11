from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# initialize the limiter
limiter = Limiter(
    key_func = get_remote_address, #use remote IP for rate limiting
    default_limits=["200 per day", "50 per hour"]  # Global default limits
)