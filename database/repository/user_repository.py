from ..utils.db_connector import database_connection


class User:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def save(self):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                           INSERT INTO User (first_name, last_name, email)
                           VALUES (%s, %s, %s)
                           """, (self.first_name, self.last_name, self.email))
            connection.commit()
            return cursor.lastrowid


    @staticmethod
    def get_all():
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM User")
            return cursor.fetchall()

    @staticmethod
    def get_by_email(email):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
            return cursor.fetchone()

    @staticmethod
    def update_name(new_name, user_id):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("UPDATE User SET first_name = %s WHERE user_id = %s", (new_name, user_id,))
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def update_last_name(new_last_name, user_id):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("UPDATE User SET last_name = %s WHERE user_id = %s", (new_last_name, user_id,))
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def update_view_mode(user_id):
        pass


