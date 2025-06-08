from ..utils.db_connector import database_connection

class Tag:
    def __init__(self, name, description=None, note=None):
        self.name = name
        self.description = description
        self.note = note

    def save(self):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                           INSERT INTO Tag (name, description, note)
                           VALUES (%s, %s, %s)
                           """, (self.name, self.description, self.note))
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Tag")
            return cursor.fetchall()

    @staticmethod
    def get_by_id(tag_id):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Tag WHERE tag_id = %s", (tag_id,))
            return cursor.fetchone()
        
    
    