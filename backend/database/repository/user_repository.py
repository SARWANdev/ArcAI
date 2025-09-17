import pymongo

from database.repository.date_time_utils import get_utc_zulu_timestamp
from database.utils.mongo_connector import mongo_connection

from model.user_profile.user import User


class UserRepository:

    @staticmethod
    def save(user: User) -> str:
        """
        this method saves a user into the mongo database

        :param user: is an instance of the class User
        :return: the id of the user or empty string if the user was not saved
        """
        with mongo_connection() as database_connection:
            try:
                result = database_connection.users.insert_one( user.new_user_dict() )
                user_id = str(result.inserted_id)
                return user_id
            except pymongo.errors.DuplicateKeyError:
                user_id = user.new_user_dict().get("_id")
                print(f"User {user_id} already exists")
                return str()

    @staticmethod
    def get_user_by_id(user_id: str) -> dict:
        """
        this method returns the user from the mongo database

        :param user_id: is the id of the user
        :return: a dictionary of the user
        """
        try:
            with mongo_connection() as db:
                return db.users.find_one({"_id": user_id })
        except Exception as e:
            print(f"Database error: {str(e)}")
            raise

    @staticmethod
    def update_view_mode(user_id: str, view_mode: bool) -> bool:
        """
        this method updates the view mode of the user either hell mode or dark mode

        :param user_id: is the id of the user
        :param view_mode: true is hell mode and false is dark mode
        :return: true if update was successful
        """
        try:
            with mongo_connection() as db:
                result = db.users.update_one({"_id": user_id},
                                             {"$set": {"view_mode": view_mode, "updated_at": get_utc_zulu_timestamp()}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Error updating users view mode: {str(e)}")
            return False

    @staticmethod
    def deactivate_user(user_id: str):
        """
        this method deactivates a user from the mongo database

        :param user_id: is the id of the user
        :return: true if deactivation was successful
        """
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
        """
        this method activates a user from the mongo database

        :param user_id: is the id of the user
        :return: true if activation was successful
        """
        try:
            with mongo_connection() as db:
                result = db.users.update_one({"_id": user_id},
                                             {"$set": {"active": True, "updated_at": get_utc_zulu_timestamp()}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Error deactivating the account: {str(e)}")
            return False

    @staticmethod
    def get_view_mode(user_id: str) -> bool:
        try:
            with mongo_connection() as db:
                result = db.users.find_one({"_id": user_id}, { "view_mode": 1 }).get("view_mode")
                return bool(result)
        except Exception as e:
            print(f"Error getting view mode: {str(e)}")
            return False
        
    @staticmethod
    def user_exists(user_id) -> bool:
        try:
            with mongo_connection() as db:
                result = db.users.find_one(str(user_id))
                return result is not None
        except Exception as e:
            print(f"User could not be retrieved: {e}")
            return False