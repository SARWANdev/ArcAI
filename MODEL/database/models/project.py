from ..utils.db_connector import database_connection


class Project:
    def __init__(self, user_id, name, description=None, note=None):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.note = note

    def save(self):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                           INSERT INTO Project (user_id, name, description, note)
                           VALUES (%s, %s, %s, %s)
                           """, (self.user_id, self.name, self.description, self.note))
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def get_by_user(user_id):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Project WHERE user_id = %s", (user_id,))
            return cursor.fetchall()

    @staticmethod
    def get_by_id(project_id):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Project WHERE project_id = %s", (project_id,))
            return cursor.fetchone()