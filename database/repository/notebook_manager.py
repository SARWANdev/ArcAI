from ..utils.db_connector import database_connection

class Notebook:
    def __init__(self, name, description=None, note=None):
        self.name = name

    def save(self):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                           INSERT INTO Notebook (name, description, note)
                           VALUES (%s, %s, %s)
                           """, (self.name, self.description, self.note))
            connection.commit()
            return cursor.lastrowid
    
    @staticmethod
    def get_by_id(notebook_id):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Notebook WHERE notebook_id = %s", (notebook_id,))
            return cursor.fetchone()
        
    