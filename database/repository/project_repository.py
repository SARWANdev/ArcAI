from database.utils.mongo_connector import mongo_connection
from datetime import datetime



class Project:
    def __init__(self, user_id, name, note=None):
        self.user_id = user_id
        self.name = name
        self.note = note

        self.created_at = datetime.utcnow().isoformat() + "Z"  # ISO 8601 with Zulu time
        self.updated_at = self.created_at

    def new_project(self):
        with mongo_connection() as db:
            project_data = {
                "user_id": self.user_id,  # Google's unique 'sub'
                "name": self.name,
                "note": self.note,
                "created_at": self.created_at,  # ISO 8601 UTC
                "updated_at": self.updated_at
            }
            result = db.projects.insert_one(project_data)
            return str(result.inserted_id)

    @staticmethod
    def get_project_by_user_id(user_id: str) -> dict:
        try:
            with mongo_connection as db:
                return db.projects.find_one({"user_id": user_id})
        except Exception as e:
            print(e)
            raise


    @staticmethod
    def get_project_by_id(project_id: str) -> dict:
        try:
            with mongo_connection as db:
                return db.projects.find_one({"_id": project_id})
        except Exception as e:
            print(e)
            raise

    @staticmethod
    def get_project_by_name(project_name: str) -> dict:
        try:
            with mongo_connection as db:
                return db.projects.find_one({"project_name": project_name})
        except Exception as e:
            raise

    @staticmethod
    def update_name(project_id, new_name):
        try:
            with mongo_connection as db:
                db.projects.update_one({"_id": project_id}, {"$set": {"name": new_name}})
        except Exception as e:
            print(e)



