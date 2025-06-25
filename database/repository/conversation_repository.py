from ..utils.db_connector import database_connection


class ConversationRepository:
    def __init__(self, user_id, name, last_opened):
        self.user_id = user_id
        self.name = name
        self.list_of_documents = []       # List of document IDs or paths
        self.human_messages = []          # List of strings
        self.ai_messages = []  

    def new_conversation(self):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO Conversation (user_id, name, last_opened)
                VALUES (%s, %s, %s, %s)
            """, (self.user_id, self.name, self.embeddings_path, self.note))
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def get_conversations_by_user_id(user_id):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM Conversation
                WHERE user_id = %s
            """, (user_id,))
            return cursor.fetchall()

    @staticmethod
    def get_conversation_by_user_id(user_id):
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM Conversation
                WHERE user_id = %s
            """, (user_id,))
            return cursor.fetchone()

    @staticmethod
    def update_conversation_name(conversation_id, new_name):
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Conversation
                SET name = %s
                WHERE conversation_id = %s
            """, (new_name, conversation_id))
            connection.commit()
            return cursor.rowcount

    @staticmethod
    def update_list_of_documents(conversation_id, list_of_documents):
        pass

    @staticmethod
    def update_human_messages(conversation_id, human_messages):
        pass

    @staticmethod
    def update_ai_messages(conversation_id, ai_messages):
        pass


