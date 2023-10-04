from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_CONNECTION_STRING")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
