from contextlib import contextmanager
from pymongo import MongoClient
from .mongo_configuration import MONGO_CONFIG


@contextmanager
def mongo_connection():
    client = MongoClient(MONGO_CONFIG["URI"])
    try:
        db = client[MONGO_CONFIG["DB_NAME"]]
        yield db
    finally:
        client.close()
