
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from database.utils.mongo_connector import mongo_connection
from database.utils.db_setup import es
from database.repository.date_time_utils import get_utc_zulu_timestamp

class ConversationRepository:
    """
    Repository class for handling conversations in MongoDB and Elasticsearch.
    This class provides methods for saving, retrieving, deleting, and updating conversations.
    It also includes methods to sync with Elasticsearch for search functionality.
    """

    @staticmethod
    def save(conversation_data: dict):
        """
        Saves a new conversation to the database and optionally adds it to Elasticsearch.

        :param conversation_data: The data of the conversation to save.
        :type conversation_data: dict

        :returns: The ID of the saved conversation.
        :rtype: str

        :raises DuplicateKeyError: If a conversation with the same unique fields already exists.
        """
        with mongo_connection() as db:
            try:
                result = db.conversations.insert_one(conversation_data)
                conversation_id = str(result.inserted_id)
                if not conversation_data.get("document_id"):
                    user_id = str(conversation_data["user_id"])
                    name = conversation_data["name"]
                    ConversationRepository.add_to_es(conversation_id, name, user_id)
                return conversation_id
            except DuplicateKeyError:
                print("Conversation already exists")
                existing_conversation = db.conversations.find_one({
                "user_id": conversation_data["user_id"],
                "name": conversation_data.get("name"),
                "document_ids": conversation_data.get("document_ids")
            })
            if existing_conversation:
                return str(existing_conversation["_id"])
                
    @staticmethod
    def add_to_es(id, name, user_id):
        """
        Adds a conversation to Elasticsearch for search purposes.

        :param id: The ID of the conversation.
        :param name: The name of the conversation.
        :param user_id: The ID of the user associated with the conversation.
        """
        es.index(index="conversations", id=id, body={
                    "user_id": user_id,
                    "name": name,
                    "suggest": {"input": name}
                })

    @staticmethod
    def get_conversation_by_id(conversation_id):
        """
        Retrieves a conversation from the database by its ID.

        :param conversation_id: The ID of the conversation to retrieve.

        :returns: The conversation data if found, otherwise None.
        :rtype: dict | None
        """
        with mongo_connection() as db:
            return db.conversations.find_one({"_id": ObjectId(conversation_id)})

    @staticmethod
    def get_user_conversations(user_id):
        with mongo_connection() as db:
            filter_query = {
                    "user_id": user_id,
                    "document_id": None
                }
            return list(db.conversations.find(filter_query))
        
    @staticmethod
    def get_conversation_by_name(name):
        """
        Retrieves a conversation from the database by its name.

        :param name: The name of the conversation to retrieve.
        :type name: str

        :returns: The conversation data if found, otherwise None.
        :rtype: dict | None
        """
        with mongo_connection() as db:
            return db.conversations.find_one({"name": name})
    
    @staticmethod
    def get_conversation_by_document(document_id):
        """
        Retrieves a conversation associated with a specific document.

        :param document_id: The ID of the document to find the associated conversation for.

        :returns: The conversation data if found, otherwise None.
        :rtype: dict | None
        """
        with mongo_connection() as db:
            return db.conversations.find_one({"document_id": document_id})
        
        
    @staticmethod
    def delete_conversation(conversation_id):
        """
        Deletes a conversation from the database and Elasticsearch.

        :param conversation_id: The ID of the conversation to delete.
        :type conversation_id: str

        :returns: True if the conversation was deleted, otherwise False.
        :rtype: bool
        """
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
    def delete_conversation_for_document(document_id):
        """
        Deletes a conversation associated with a specific document.

        :param document_id: The ID of the document associated with the conversation to delete.
        :type document_id: str

        :returns: True if the conversation was deleted, otherwise False.
        :rtype: bool
        """
        try:
            with mongo_connection() as db:
                result = db.conversations.delete_one({"document_id": document_id})
                return result.deleted_count > 0
        except Exception as e:
            print(f"Conversation could not be deleted: {e}")
            return False

    @staticmethod
    def clear_history(user_id):
        """
        Clears all conversations for a user that are not associated with a document.

        :param user_id: The ID of the user whose conversation history to clear.
        :type user_id: str

        :returns: True if the conversation history was cleared, otherwise False.
        :rtype: bool
        """
        try:
            with mongo_connection() as db:
                filter_query = {
                    "user_id": user_id,
                    "document_id": None
                }

                result = db.conversations.delete_many(filter_query)
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
    def delete_all_conversations(user_id):
        """
        Deletes all conversations for a user from the database and Elasticsearch.

        :param user_id: The ID of the user whose conversations to delete.
        :type user_id: str

        :returns: True if all conversations were deleted, otherwise False.
        :rtype: bool
        """
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
        """
        Updates the name of a conversation.

        :param conversation_id: The ID of the conversation to update.
        :type conversation_id: str
        :param new_name: The new name to assign to the conversation.
        :type new_name: str

        :returns: True if the conversation name was updated, otherwise False.
        :rtype: bool
        """
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
        """
        Updates the list of documents associated with a conversation.

        :param conversation_id: The ID of the conversation to update.
        :type conversation_id: str
        :param list_of_documents: The new list of document IDs to associate with the conversation.
        :type list_of_documents: list

        :returns: True if the list of documents was updated, otherwise False.
        :rtype: bool
        """
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
        """
        Updates the messages of a conversation.

        :param conversation_id: The ID of the conversation to update.
        :type conversation_id: str
        :param messages: The new list of messages to assign to the conversation.
        :type messages: list

        :returns: True if the messages were updated, otherwise False.
        :rtype: bool
        """
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
    def search_conversation(user_id, query):
        """
        Searches for conversations by their title using Elasticsearch.

        :param user_id: The ID of the user to filter conversations by.
        :type user_id: str
        :param query: The search query to match against conversation names.
        :type query: str

        :returns: A list of matching conversation IDs and names.
        :rtype: list[dict]
        """
        es.indices.refresh(index="conversations")
        result = es.search(index="conversations", body={
            "size": 4,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_phrase_prefix": {
                                "name": {
                                    "query": query
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