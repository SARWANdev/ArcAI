from bson import ObjectId
from database.utils.mongo_connector import mongo_connection

class DocumentPropertiesRepository:

    @staticmethod
    def mark_as_favorite(document_id) -> bool:
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"favorite": True}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Document could not be mark as favorite: {e}")
            return False


    @staticmethod
    def mark_as_not_favorite(document_id) -> bool:
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"favorite": False}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Document could not be mark as not favorite: {e}")
            return False

    @staticmethod
    def mark_as_read(document_id):
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"read": True}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Document could not be mark as read: {e}")
            return False

    @staticmethod
    def mark_as_not_read(document_id) -> bool:
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"read": False}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Document could not be mark as read: {e}")
            return False

    @staticmethod
    def update_journal(document_id, journal_name) -> bool:
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"journal": journal_name}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Journal name could not be update: {e}")
            return False

    @staticmethod
    def update_first_author(document_id, first_author_name) -> bool:
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"first_author": first_author_name}})
                return result.modified_count > 0
        except Exception as e:
            print(f"First author name could not be update: {e}")
            return False

    @staticmethod
    def update_tag(document_id, tag_name) -> bool:
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"tag_name": tag_name}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Tag name could not be update: {e}")
            return False

    @staticmethod
    def update_tag_color(document_id, tag_color) -> bool:
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"tag_color": tag_color}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Tag name could not be update: {e}")
            return False

    @staticmethod
    def set_new_project_id(document_id, new_project_id) -> bool:
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"project_id": new_project_id}})
                return result.modified_count > 0
        except Exception as e:
            print(f"New project id could not be set: {e}")
            return False

