from ..utils.db_connector import database_connection


class Document:
    def __init__(self, project_id, name, path, note=None):
        self.project_id = project_id
        self.name = name
        self.path = path
        self.note = note

    def save(self):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                           INSERT INTO Document (project_id, name, path, note)
                           VALUES (%s, %s, %s, %s)
                           """, (self.project_id, self.name, self.path, self.note))
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def get_by_project(project_id):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Document WHERE project_id = %s", (project_id,))
            return cursor.fetchall()

    @staticmethod
    def get_by_id(document_id):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Document WHERE document_id = %s", (document_id,))
            return cursor.fetchone()