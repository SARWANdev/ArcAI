import pymongo
from pymongo.errors import DuplicateKeyError
from database.utils.mongo_connector import mongo_connection
from database.utils.db_setup import es

class ConversationRepository:
    def __init__(self, user_id, name, last_opened):
        self.user_id = user_id
        self.name = name
        #TODO solve how the convos are gonna be stored
        self.list_of_documents = []       # List of document IDs or paths
        self.human_messages = []          # List of strings
        self.ai_messages = []
        self.last_opened = last_opened

    def new_conversation(self):
        conversation_data = {"user_id": self.user_id, "name": self.name, "last_opened": self.last_opened,
                             "list_of_documents": self.list_of_documents, "human_messages": self.human_messages}
        with mongo_connection as db:
            try:
                #Add to MongoDB
                result = db.conversations.insert_one(conversation_data)
                id = result.inserted_id
                #Add to Elasticsearch
                es.index("conversations", id=id, body={
                    "user_id": self.user_id,
                    "name": self.name,
                    "suggest": {
                        "input": self.name
                    }
                })
            except pymongo.errors.DuplicateKeyError:
                print("Conversation already exists")


    @staticmethod
    def get_conversations_by_user_id(user_id):
        with mongo_connection() as db:
            return list (db.projects.find({"user_id": user_id}))

    @staticmethod
    def get_conversation_by_id(conversation_id):
        with mongo_connection() as db:
            return db.conversations.find_one({"_id": conversation_id})
        
    @staticmethod
    def delete_conversation(conversation_id):
        try:
            with mongo_connection() as db:
                result = db.conversations.delete_one({"_id": conversation_id})
                es.delete(index = "conversations", id = conversation_id)
                return result.deleted_count > 0
        except Exception as e:
            print(f"Conversation could not be deleted: {e}")
            return False
        
    @staticmethod
    def delete_all_conversations(user_id):
        try:
            with mongo_connection() as db:
                result = db.conversations.delete_many({"user_id": user_id})
                es.delete_by_query(index = "conversations", body={
                    "query": {
                        "term": {
                            "user_id": user_id
                        }
                    }
                })
                return result.deleted_count > 0
        except Exception as e:
            print(f"Chat history could not be deleted: {e}")
            return False

    @staticmethod
    def update_conversation_name(conversation_id, new_name) -> bool:
        try:
            with mongo_connection() as db:
                result = db.conversations.update_one({"_id": conversation_id},
                                                     {"$set": {"name": new_name}})
                es.update(index = "conversations", id = conversation_id, body={
                    "doc": {"name": new_name}
                })
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
    def add_user_message(conversation_id, message) -> bool:
        try:
            with mongo_connection() as db:
                new_message = {"role": "user", "content": message}
                result = db.conversations.update_one({"_id": conversation_id},
                                                     {"$push": {"messages": new_message}})
                return result.modified_count > 0
        except Exception as e:
            print(f"ERROR: Updating human messages {e}")
            return False


    @staticmethod
    def add_ai_message(conversation_id, message):
        try:
            with mongo_connection() as db:
                new_message = {"role": "ai", "content": message}                
                result = db.conversations.update_one({"_id": conversation_id},
                                                     {"$push": {"messages": new_message}})
                return result.modified_count > 0
        except Exception as e:
            print(f"ERROR: Updating ai messages {e}")
            return False

    @staticmethod
    def search_conversation(user_id, prefix):
        # Searchs for a conversation by its title
        result = es.search(index="conversations", body={
            "size": 4,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_phrase_prefix": {
                                "name": {
                                    "query": prefix
                                }
                            }
                        }
                    ],
                    "filter": [
                        { "term": { "user_id": user_id } }
                    ]
                }
            }
        })
        hits = result["hits"]["hits"]
        return [
            {"id": hit["_id"], "name": hit["_source"].get("name", "")}
            for hit in hits
        ]