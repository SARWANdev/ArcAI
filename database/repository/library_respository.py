from ..utils.db_connector import database_connection

class Library:
    def __init__(self,  description=None, note=None):
        self.description = description
        self.note = note

    def save(self):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                           INSERT INTO Library (description, note)
                           VALUES (%s, %s)
                           """, (self.description, self.note))
            connection.commit()
            return cursor.lastrowid
        
    @staticmethod
    def get_by_id(library_id):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Library WHERE library_id = %s", (library_id,))
            return cursor.fetchone()
        
    @staticmethod
    def get_by_user(user_id):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM User WHERE user_id = %s", (user_id,))
            return cursor.fetchall()
