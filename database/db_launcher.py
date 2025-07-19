from pymongo import ASCENDING
from utils.mongo_connector import mongo_connection
from utils.db_setup import es

def init_es():
    # Creates Elasticsearch indices
    if not (es.indices.exists(index = "documents") and es.indices.exists(index = "conversations")):
        es.indices.create(index="documents", body={
            "mappings": {
                "properties": {
                    "user_id":{"type": "text"},
                    "name": {"type": "text"},
                    "author": {"type": "text"},
                    "suggest": {"type": "completion"}
                }
            }
        })
        es.indices.create(index = "conversations", body={
            "mappings": {
                "properties": {
                    "user_id":{"type": "text"}, 
                    "name": {"type": "text"},
                    "suggest": {"type": "completion"}
                }
            }
        })
        print("Elasticsearch indices created")
    else:
        print("Elasticsearch indices already exist")



def init_mongo():
    with mongo_connection() as db:

        # --------------------
        # USERS collection
        # --------------------
        db.users.create_index([("email", ASCENDING)], unique=True)

        # --------------------
        # PROJECTS collection
        # --------------------
        db.projects.create_index([("user_id", ASCENDING)])

        # --------------------
        # DOCUMENTS collection
        # --------------------
        db.documents.create_index([("project_id", ASCENDING)])
        db.documents.create_index([("favorite", ASCENDING)])
        db.documents.create_index([("read", ASCENDING)])
        # optional: text index for full-text search over journals / note / bibtex
        # db.documents.create_index([("journal", "text"), ("note", "text"), ("bibtex", "text")])

        # --------------------
        # DOCUMENTS collection
        # --------------------
        db.pdf_master.create_index([("hash", ASCENDING)])  # Ensure deduplication , unique=True
        db.pdf_master.create_index([("ref_count", ASCENDING)])

        # --------------------
        # CONVERSATIONS collection
        # --------------------
        db.conversations.create_index([("user_id", ASCENDING)])
        db.conversations.create_index([("last_opened", ASCENDING)])

        print("MongoDB indexes created")


if __name__ == "__main__":
    init_mongo()
    init_es()




