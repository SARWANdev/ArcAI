
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from database.utils.mongo_connector import mongo_connection
from database.utils.db_setup import es
from database.repository.date_time_utils import get_utc_zulu_timestamp

class ConversationRepository:
 
    @staticmethod
    def save(conversation_data: dict):
        with mongo_connection() as db:
            try:
                result = db.conversations.insert_one(conversation_data)
                conversation_id = str(result.inserted_id)
                user_id = str(conversation_data["user_id"])
                name = conversation_data["name"]
                ConversationRepository.add_to_es(conversation_id, name, user_id)
                return conversation_id
            except DuplicateKeyError:
                print("Conversation already exists")
                existing_conversation = db.conversations.find_one({
                "user_id": conversation_data["user_id"],
                "name": conversation_data.get("name"),
                # Add other unique fields that might cause the duplicate
                "document_ids": conversation_data.get("document_ids")
            })
            if existing_conversation:
                return str(existing_conversation["_id"])
                
    @staticmethod
    def add_to_es(id, name, user_id):
        es.index(index="conversations", id=id, body={
                    "user_id": user_id,
                    "name": name,
                    "suggest": {"input": name}
                })

    
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
    def delete_all_conversations(user_id):
        try:
            with mongo_connection() as db:
                filter_query = {
                    "user_id": user_id,
                    "document_id": {"$ne": None}
                }

                result = db.conversations.delete_many({filter_query})
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
                db.coversations.update_one({"_id": ObjectId(conversation_id)},
                                           {"$set": {"updated_at": get_utc_zulu_timestamp()}})
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