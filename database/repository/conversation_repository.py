
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from database.utils.mongo_connector import mongo_connection
from database.utils.db_setup import es

class ConversationRepository:
 
    @staticmethod
    def save(conversation_data: dict) -> str:
        with mongo_connection() as db:
            try:
                result = db.conversations.insert_one(conversation_data)
                conversation_id = str(result.inserted_id)
                es.index(index="conversations", id=conversation_id, body={
                    "user_id": conversation_data["user_id"],
                    "name": conversation_data["name"],
                    "suggest": {"input": conversation_data["name"]}
                })
                return conversation_id
            except DuplicateKeyError:
                print("Conversation already exists")
                return ""


    @staticmethod
    def get_conversations_by_user_id(user_id):
        with mongo_connection() as db:
            return list (db.conversations.find({"user_id": user_id}))

    @staticmethod
    def get_history(user_id):
        
        es.indices.refresh(index="conversations")
        query = {
            "query": {
                "match": {
                    "user_id": user_id
                }
            }
        }
        result = es.search(index="conversations", body=query)
        return [doc['_source'] for doc in result['hits']['hits']]

    @staticmethod
    def add_to_history(conversation_data: dict):
        id = conversation_data.get("_id")
        result = es.index(index="conversations", id=id, body={
                    "user_id": conversation_data["user_id"],
                    "name": conversation_data["name"],
                    "suggest": {"input": conversation_data["name"]}
                })
        return result["result"] == "created" or result["result"] == "updated"

    @staticmethod
    def get_conversation_by_id(conversation_id):
        with mongo_connection() as db:
            return db.conversations.find_one({"_id": ObjectId(conversation_id)})

    @staticmethod
    def get_user_conversations(user_id):
        with mongo_connection() as db:
            return list(db.conversations.find({"user_id": user_id}))
        
    @staticmethod
    def get_conversation_by_name(name):
        with mongo_connection() as db:
            return db.conversations.find_one({"name": name})
        
    @staticmethod
    def delete_conversation(conversation_id):

        try:
            with mongo_connection() as db:
                result = db.conversations.delete_one({"_id": ObjectId(conversation_id)})
                if es.exists(index="conversations", id=conversation_id):
                    es.delete(index = "conversations", id = conversation_id)
                return result.deleted_count > 0
        except Exception as e:
            print(f"Conversation could not be deleted: {e}")
            return False
    
    @staticmethod
    def clear_history(self, user_id):
        history = self.get_history(user_id)
        try:
            with mongo_connection() as db:
                for conversation in history:
                    id = conversation["_id"]
                    result = db.conversations.delete_one({"_id": ObjectId(id)})
                    es.delete(index = "conversations", id = id)
                return result.deleted_count > 0
        except Exception as e:
            print(f"History could not be cleared: {e}")
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
                result = db.conversations.update_one({"_id": ObjectId(conversation_id)},
                                                     {"$set": {"name": new_name}})
                if es.exists(index="conversations", id=conversation_id):
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
                result = db.conversations.update_one({"_id": ObjectId(conversation_id)},
                                                     {"$set": {"list_of_documents": list_of_documents}})
                return result.modified_count > 0
        except Exception as e:
            print(f"ERROR: Updating conversation list of documents {e}")
            return False


    @staticmethod
    def update_messages(conversation_id, messages: list) -> bool:
        try:
            with mongo_connection() as db:
                result = db.conversations.update_one({"_id": ObjectId(conversation_id)},
                                                    {"$set": {"messages": messages}})
                return result.modified_count > 0
        except Exception as e:
            print(f"ERROR: Updating conversation messages {e}")
            return False


    @staticmethod
    def search_conversation(user_id, prefix):
        # Searchs for a conversation by its title
        es.indices.refresh(index="conversations")
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