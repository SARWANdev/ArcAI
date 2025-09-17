from contextlib import contextmanager
from pymongo import MongoClient
from .mongo_configuration import MONGO_CONFIG


@contextmanager
def mongo_connection():
    """
    Establishes a connection to the MongoDB database using the configuration.

    :returns: A MongoDB database connection object.
    :rtype: pymongo.database.Database
    
    :raises: MongoClientError if there is an issue connecting to the database.
    """
    client = MongoClient(MONGO_CONFIG["URI"])
    try:
        db = client[MONGO_CONFIG["DB_NAME"]]
        yield db
    finally:
        client.close()
