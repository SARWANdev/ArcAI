from pymongo import MongoClient
from contextlib import contextmanager


client = MongoClient("mongodb://localhost:27017/")
db = client["arcai1"]
users = db["users"]
projects = db["projects"]
documents = db["documents"]
conversations = db["conversations"]



