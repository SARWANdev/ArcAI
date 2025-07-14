from pymongo import MongoClient
from contextlib import contextmanager
from elasticsearch import Elasticsearch


client = MongoClient("mongodb://localhost:27017/")
db = client["arcai1"]
users = db["users"]
projects = db["projects"]
documents = db["documents"]
conversations = db["conversations"]

es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "TB=IE8CncAGH6+2jG48w")) #JUST FOR DANI