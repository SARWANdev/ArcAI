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
        
