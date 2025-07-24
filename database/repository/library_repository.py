from database.utils.mongo_connector import mongo_connection

class Library:
    """
    Library repository module for handling user library operations in the database.

    Provides methods to interact with the user's library stored in the database.
    """
    @staticmethod
    def get_user_library(user_id) -> list:
        """
        Retrieve the library (projects) for a specific user from the database.

        :param user_id: The unique identifier of the user whose library is to be retrieved.
        :type user_id: str or ObjectId
        :return: A list of projects belonging to the user.
        :rtype: list
        """
        with mongo_connection() as db:
            return list(db.projects.find({"user_id": user_id}))
