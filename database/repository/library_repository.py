from database.utils.mongo_connector import mongo_connection

class Library:
    
    @staticmethod
    def get_user_library(user_id) -> list:
        with mongo_connection() as db:
            return list(db.projects.find({"user_id": user_id}))
