import secrets

# Generate a random salt during program startup
GLOBAL_SALT = secrets.token_urlsafe(16)
