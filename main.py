# main.py
import os
from fastapi import FastAPI
from Explorari.routes.v1 import users
from Database import setup_mongodb
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# MongoDB Configuration
MONGO_URI = os.environ.get("MONGO_CONNECTION_STRING")
DB_NAME = os.environ.get("MONGO_DB_NAME")

# Setup MongoDB connection
setup_mongodb(app, MONGO_URI, DB_NAME)

# Include API routes
app.include_router(users.router, prefix="/v1/users")
