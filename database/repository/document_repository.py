from ..utils.db_setup import database_connection


class Document:
    def __init__(self, project_id, name, path, embeddings_path, note=None):
        self.project_id = project_id
        self.name = name
        self.path = path
        self.embeddings_path = embeddings_path
        self.note = note

    def new_document(self):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                           INSERT INTO Document (project_id, name, path, embeddings_path, note)
                           VALUES (%s, %s, %s, %s, %s)
                           """, (self.project_id, self.name, self.path, self.embeddings_path, self.note))
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def get_by_project(project_id):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Document WHERE project_id = %s", (project_id,))
            return cursor.fetchall()

    @staticmethod
    def get_by_document_id(document_id):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Document WHERE document_id = %s", (document_id,))
            return cursor.fetchone()

    @staticmethod
    def update_document_name(document_id, name):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE Document SET name = %s WHERE document_id = %s", (name, document_id,))
            connection.commit()
            return cursor.lastrowid
    @staticmethod
    def update_path(document_id, path):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE Document SET path = %s WHERE document_id = %s", (path, document_id,))
            connection.commit()
            return cursor.lastrowid
        
    @staticmethod
    def update_embeddings_path(document_id, embeddings_path):
        pass
    @staticmethod
    def get_bibtex_by_document_id(document_id):
        pass
    @staticmethod
    def update_bibtex(document_id, bibtex):
        pass
