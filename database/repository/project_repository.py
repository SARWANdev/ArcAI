from ..utils.db_setup import database_connection


class Project:
    def __init__(self, user_id, name, description=None, note=None):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.note = note

    def new_project(self):
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

    @staticmethod
    def get_by_name(name):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Project WHERE name = %s", (name,))
            return cursor.fetchall()

    @staticmethod
    def update_name(project_id, name):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                           UPDATE Project
                           SET name = %s
                           WHERE project_id = %s
                           """, (name, project_id))
            connection.commit()
            return cursor.rowcount # Returns 1 if updated, 0 if no project found

    @staticmethod
    def update_description(project_id, description):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                           UPDATE Project
                           SET description = %s
                           WHERE project_id = %s
                           """, (description, project_id))
            connection.commit()
            return cursor.rowcount # Returns 1 if updated, 0 if no project found



