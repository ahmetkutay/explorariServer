import os
from dotenv import load_dotenv, set_key

load_dotenv()

MONGO_URI = os.getenv("MONGO_CONNECTION_STRING")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE_MINUTES = os.getenv("JWT_EXPIRES_IN")
ENCRYPT_PASSWORD = os.getenv("ENCRYPT_PASSWORD")
ENCRYPTION_SALT = os.getenv("ENCRYPTION_SALT")
if ENCRYPTION_SALT is None:
    ENCRYPTION_SALT = os.urandom(16).hex()
    set_key('.env', 'ENCRYPTION_SALT', ENCRYPTION_SALT)
