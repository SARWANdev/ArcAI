from ..utils.db_connector import database_connection

class DocumentPropertiesRepository:

    
    @staticmethod
    def mark_as_favorite(project_id):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE Document SET is_it_favorite = 1 WHERE project_id = %s", (project_id,))
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def mark_as_not_favorite(project_id):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE Document SET is_it_favorite = 0 WHERE project_id = %s", (project_id,))
            connection.commit()
            return cursor.lastrowid


    @staticmethod
    def mark_as_read(project_id):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE Document SET is_it_read = 1 WHERE project_id = %s", (project_id,))
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def mark_as_not_read(project_id):
        pass

    @staticmethod
    def update_journal(journal_name, document_id):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE Document SET journal = %s WHERE document_id = %s", (journal_name, document_id))
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def update_first_author(first_author_name, document_id):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE Document SET first_author = %s WHERE document_id = %s", (first_author_name, document_id))
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def update_tag(tag_name, document_id):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE Document SET tag = %s WHERE document_id = %s", (tag_name, document_id))
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def update_tag_color(tag_color, document_id):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE Document SET tag_color = %s WHERE document_id = %s", (tag_color, document_id))
            connection.commit()
            return cursor.lastrowid

        
    
    