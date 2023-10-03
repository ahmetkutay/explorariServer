# db/__init__.py
from fastapi import FastAPI
from .mongoDBConnection import connect_to_mongo


def setup_mongodb(app: FastAPI, mongo_uri: str, db_name: str):
    return connect_to_mongo(app, mongo_uri, db_name)
