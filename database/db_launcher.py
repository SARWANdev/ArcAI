from pymongo import ASCENDING
from utils.mongo_connector import mongo_connection


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
        # CONVERSATIONS collection
        # --------------------
        db.conversations.create_index([("user_id", ASCENDING)])
        db.conversations.create_index([("last_opened", ASCENDING)])

        print("MongoDB indexes created")


if __name__ == "__main__":
    init_mongo()




