from ..utils.db_connector import database_connection

class Notebook:

    @staticmethod
    def get_project_notebook(project_id):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT note FROM Project WHERE project_id = %s", (project_id,))
            return cursor.fetchone()

    @staticmethod
    def update_project_notebook(project_id, note):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE Project SET note = %s WHERE project_id = %s", (note, project_id,))
            connection.commit()
            return cursor.rowcount

    @staticmethod
    def get_document_notebook(document_id):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT note FROM Document WHERE document_id = %s", (document_id,))
            return cursor.fetchone()

    @staticmethod
    def update_document_notebook(document_id, note):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE Document SET note = %s WHERE document_id = %s", (note, document_id,))
            connection.commit()
            return cursor.rowcount


        
    