import pymongo
import pymongo.errors

from database.repository.date_time_utils import get_utc_zulu_timestamp
from database.utils.mongo_connector import mongo_connection
from bson import ObjectId




class Project:
    def __init__(self, user_id, project_name, note=None):
        self.user_id = user_id
        self.project_name = project_name
        self.note = note

        self.created_at = get_utc_zulu_timestamp()
        self.updated_at = self.created_at

    def new_project(self):
        project_data = {
            "user_id": self.user_id,  # Google's unique 'sub'
            "project_name": self.project_name,
            "note": self.note,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        with mongo_connection() as db:
            try:
                result = db.projects.insert_one(project_data)
                return str(result.inserted_id)
            except pymongo.errors.DuplicateKeyError:
                print(f"Project {self.project_name} already exists")
                return None


    @staticmethod
    def get_project_by_user_id(user_id: str) -> dict:
        try:
            with mongo_connection() as db:
                return db.projects.find_one({"user_id": user_id})
        except Exception as e:
            print(e)
            raise


    @staticmethod
    def get_project_by_id(project_id: str) -> dict:
        try:
            with mongo_connection() as db:
                # Convert to ObjectId if it's a string
                if isinstance(project_id, str):
                    project_id = ObjectId(project_id)
                return db.projects.find_one({"_id": project_id})
        except Exception as e:
            print(e)
            raise

    @staticmethod
    def get_project_by_name(project_name: str) -> dict:
        try:
            with mongo_connection() as db:
                return db.projects.find_one({"project_name": project_name})
        except Exception as e:
            print(f"Error getting project by name: {str(e)}")
            raise

    @staticmethod
    def update_name(project_id, new_name) -> bool:
        try:
            with mongo_connection() as db:
                result = db.projects.update_one({"_id": project_id}, {"$set": {"project_name": new_name,
                                                                      "updated_at": get_utc_zulu_timestamp()}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Project name could not be update: {e}")
            return False

    @staticmethod
    def delete_project(project_id) -> bool:
        try:
            with mongo_connection() as db:
                # Ensure project_id is ObjectId
                if isinstance(project_id, str):
                    project_id = ObjectId(project_id)
                result = db.projects.delete_one({"_id": project_id})
                return result.deleted_count > 0
        except Exception as e:
            print(f"Project could not be deleted: {e}")
            return False



