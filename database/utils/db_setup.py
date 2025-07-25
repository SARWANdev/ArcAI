from pymongo import MongoClient
from contextlib import contextmanager
from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
load_dotenv()


client = MongoClient(os.getenv("MONGO_URI") or "mongodb://localhost:27017/")
db = client["arcai1"]
users = db["users"]
projects = db["projects"]
documents = db["documents"]
conversations = db["conversations"]

es = Elasticsearch(
    os.getenv("ELASTIC_URI", "https://127.0.0.1:9200"),
    basic_auth=(
        os.getenv("ELASTIC_USER", "elastic"),
        os.getenv("ELASTIC_PASSWORD", "ZJM0fN6SIt=Zm0=JQZ5H")
    ),
    verify_certs=False  # Ignore certified autosigned
)
