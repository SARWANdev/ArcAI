import pymongo
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from database.repository.date_time_utils import get_utc_zulu_timestamp
from database.utils.mongo_connector import mongo_connection
from typing import List, Dict

from model.user_profile.user import User


class User:
    def __init__(self, first_name, last_name, email, sub_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.sub_id = sub_id
        self.view_mode = True
        self.active = True
        self.created_at = get_utc_zulu_timestamp()
        self.updated_at = self.created_at

    def new_user(self):
        if not self.sub_id:
            raise ValueError("Google 'sub' ID is required")

        user_data = {
            "_id": self.sub_id,  # Google's unique 'sub'
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "view_mode": self.view_mode,  # Defaults to True
            "active": self.active,  # Defaults to True
            "created_at": self.created_at,  # ISO 8601 UTC
            "updated_at": self.updated_at
        }

        with mongo_connection() as database_connection:
            try:
                result = database_connection.users.insert_one(user_data)
                return str(result.inserted_id)
            except pymongo.errors.DuplicateKeyError:
                print(f"User {self.sub_id} already exists")
                return str()

    @staticmethod
    def save(user: User) -> str:
        with mongo_connection() as database_connection:
            result = database_connection.users.insert_one( user.new_user_dict() )
            user_id = str(result.inserted_id)
            return user_id
    @staticmethod
    def get_user_by_id(user_id: str) -> dict:
        try:
            with mongo_connection() as db:
                return db.users.find_one({"_id": user_id })
        except Exception as e:
            print(f"Database error: {str(e)}")
            raise

    @staticmethod
    def update_view_mode(user_id: str, view_mode: bool) -> bool:
        try:
            with mongo_connection() as db:
                result = db.users.update_one({"_id": user_id},
                                             {"$set": {"view_mode": view_mode, "updated_at": get_utc_zulu_timestamp()}})
                return result.modified_count > 0

        except Exception as e:
            print(f"Error updating users view mode: {str(e)}")
            return False

    @staticmethod
    def delete_user_contents(user_id: str):
        try:
            with mongo_connection() as db:
                result = db.users.update_one({"_id": user_id},
                                             {"$set": {"active": False, "updated_at": get_utc_zulu_timestamp()}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Error deactivating the account: {str(e)}")
            return False

    @staticmethod
    def activate_user(user_id: str):
        try:
            with mongo_connection() as db:
                result = db.users.update_one({"_id": user_id},
                                             {"$set": {"active": True, "updated_at": get_utc_zulu_timestamp()}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Error deactivating the account: {str(e)}")
            return False