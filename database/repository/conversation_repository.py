import pymongo
from pymongo.errors import DuplicateKeyError
from database.utils.mongo_connector import mongo_connection

class ConversationRepository:
    def __init__(self, user_id, name, last_opened):
        self.user_id = user_id
        self.name = name
        self.list_of_documents = []       # List of document IDs or paths
        self.human_messages = []          # List of strings
        self.ai_messages = []
        self.last_opened = last_opened

    def new_conversation(self):
        conversation_data = {"user_id": self.user_id, "name": self.name, "last_opened": self.last_opened,
                             "list_of_documents": self.list_of_documents, "human_messages": self.human_messages}
        with mongo_connection as db:
            try:
                db.conversations.insert_one(conversation_data)
            except pymongo.errors.DuplicateKeyError:
                print("Conversation already exists")


    @staticmethod
    def get_conversations_by_user_id(user_id):
        pass

    @staticmethod
    def get_conversation_by_user_id(user_id):
        pass

    @staticmethod
    def update_conversation_name(conversation_id, new_name) -> bool:
        try:
            with mongo_connection() as db:
                result = db.conversations.update_one({"_id": conversation_id},
                                                     {"$set": {"name": new_name}})
                return result.modified_count > 0
        except Exception as e:
            print(f"ERROR: Updating conversation name {e}")
            return False

    @staticmethod
    def update_list_of_documents(conversation_id, list_of_documents) -> bool:
        try:
            with mongo_connection() as db:
                result = db.conversations.update_one({"_id": conversation_id},
                                                     {"$set": {"list_of_documents": list_of_documents}})
                return result.modified_count > 0
        except Exception as e:
            print(f"ERROR: Updating conversation list of documents {e}")
            return False

    @staticmethod
    def update_human_messages(conversation_id, human_messages) -> bool:
        try:
            with mongo_connection() as db:
                result = db.conversations.update_one({"_id": conversation_id},
                                                     {"human_messages": human_messages})
                return result.modified_count > 0
        except Exception as e:
            print(f"ERROR: Updating human messages {e}")
            return False


    @staticmethod
    def update_ai_messages(conversation_id, ai_messages):
        try:
            with mongo_connection() as db:
                result = db.conversations.update_one({"_id": conversation_id},
                                                     {"ai_messages": ai_messages})
                return result.modified_count > 0
        except Exception as e:
            print(f"ERROR: Updating ai messages {e}")
            return False


