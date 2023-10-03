from pymongo import MongoClient
from pymongo.collection import Collection
from fastapi import FastAPI


class MongoDB:
    def __init__(self, app: FastAPI, mongo_uri: str, db_name: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client.get_database(name=db_name)

    def get_collection(self, collection_name: str) -> Collection:
        return self.db.get_collection(collection_name)


def connect_to_mongo(app: FastAPI, mongo_uri: str, db_name: str):
    mongodb = MongoDB(app, mongo_uri, db_name)
    app.mongodb = mongodb

    @app.on_event("shutdown")
    async def shutdown_mongo_client():
        mongodb.client.close()

    return mongodb
