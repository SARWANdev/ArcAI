from ..utils.db_setup import database_connection

class Library:
    @staticmethod
    def get_user_library(user_id):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Project WHERE user_id = %s", (user_id,))
            return cursor.fetchall()
