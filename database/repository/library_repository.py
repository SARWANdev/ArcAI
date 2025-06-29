from database.utils.mongo_connector import mongo_connection

class Library:
    # TODO: add a method that returns all documents from an user
    @staticmethod
    def get_user_library(user_id) -> dict:
        with mongo_connection() as db:
            return db.projects.find_one({"user_id": user_id})



