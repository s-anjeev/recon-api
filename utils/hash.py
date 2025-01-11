import hashlib
import hmac
# from config.config import hash_secret


def password_hash(string_to_hash):
    # Fetch the secret key from the hash_secret dictionary
    # secret = hash_secret["password"]
    secret = "asfv6s4g65fg1bfxvskdpknononkuygwdih2874iehfbnb"
    # Convert the secret key to bytes
    secret_bytes = secret.encode()
    # Generate the HMAC using SHA-256
    hashed = hmac.new(secret_bytes, string_to_hash.encode(), hashlib.sha256).hexdigest()
    return hashed