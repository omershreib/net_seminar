from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def is_mongo_available(uri="mongodb://localhost:27017"):
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        client.admin.command("ping")
        client.close()
        return True
    except ConnectionFailure:
        return False
