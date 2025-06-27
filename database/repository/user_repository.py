import pymongo
from pymongo.errors import DuplicateKeyError
from database.utils.mongo_connector import mongo_connection
from typing import List, Dict


class User:
    def __init__(self, first_name, last_name, email, sub_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.sub_id = sub_id
        self.view_mode = True
        self.is_an_active_account = True

    def new_user(self):
        if not self.sub_id:
            raise ValueError("Google 'sub' ID is required")

        user_data = {
            "_id": self.sub_id,  # Google's unique 'sub'
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "view_mode": self.view_mode,  # Defaults to True
            "is_an_active_account": self.is_an_active_account  # Defaults to True
        }

        with mongo_connection() as database_connection:
            try:
                database_connection.users.insert_one(user_data)
            except pymongo.errors.DuplicateKeyError:
                print(f"User {self.sub_id} already exists")

    @staticmethod
    def get_all_users() -> List[Dict]:
        with mongo_connection() as db:
            users = list(db.users.find({}, {'_id': 1, 'first_name': 1, 'last_name': 1,
                                            'email': 1}))
            #take care what fields are included with the boolean variables. TO CHECK
            return users

    @staticmethod
    def get_user_by_email(email: str) -> dict:
        if not email or "@" not in email:
            raise ValueError("Invalid email format")

        try:
            with mongo_connection() as db:
                return db.users.find_one({"email": email})
        except Exception as e:
            print(f"Database error: {str(e)}")
            raise

    @staticmethod
    def update_user_name(user_id: str, new_name: str) -> bool:
        try:
            with mongo_connection() as db:
                result = db.users.update_one(
                    {'_id': user_id},
                    {'$set': {
                        'first_name': new_name,
                    }}
                )
                return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return False

    @staticmethod
    def update_user_last_name(user_id: str, new_last_name: str) -> bool:
        try:
            with mongo_connection() as db:
                result = db.users.update_one(
                    {'_id': user_id},
                    {'$set': {
                        'last_name': new_last_name,
                    }}
                )
                return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return False

    @staticmethod
    def update_view_mode(user_id):
        pass




