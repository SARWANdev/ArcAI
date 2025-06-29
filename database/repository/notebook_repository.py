from database.utils.mongo_connector import mongo_connection

class Notebook:

    @staticmethod
    def get_project_notebook(project_id) -> str:
        with mongo_connection() as db:
            return db.projects.find_one({"_id": project_id})["note"]


    @staticmethod
    def update_project_notebook(project_id, note) -> bool:
        try:
            with mongo_connection() as db:
                result = db.projects.update_one({"_id": project_id}, {"$set": {"note": note}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Project notebook could not be update: {e}")
            return False


    @staticmethod
    def get_document_notebook(document_id) -> str:
        with mongo_connection() as db:
            return db.documents.find_one({"_id": document_id})["note"]


    @staticmethod
    def update_document_notebook(document_id, note) -> bool:
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": document_id}, {"$set": {"note": note}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Document notebook could not be update: {e}")
            return False


        
    