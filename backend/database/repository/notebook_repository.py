from bson import ObjectId

from database.utils.mongo_connector import mongo_connection

class Notebook:
    """
    Repository for notebook operations on projects and documents in the database.
    
    Provides static methods to get and update notebook content.
    """

    @staticmethod
    def get_project_notebook(project_id) -> str:
        """
        Retrieve the notebook content for a given project.

        :param project_id: Project identifier.
        :type project_id: str

        :return: Notebook content as a string, empty string if not found.
        :rtype: str
        """
        try:
            with mongo_connection() as db:
                project = db.projects.find_one({"_id": ObjectId(project_id)})
                if project is None:
                    return ""
                return project.get("note", "")
        except Exception as e:
            print(f"Error retrieving project notebook: {e}")
            return ""

    @staticmethod
    def update_project_notebook(project_id, note) -> bool:
        """
        Update the notebook content for a project.

        :param project_id: Project identifier.
        :type project_id: str
        :param note: New notebook content.
        :type note: str

        :return: True if update was successful, else False.
        :rtype: bool
        """
        try:
            with mongo_connection() as db:
                result = db.projects.update_one({"_id": ObjectId(project_id)}, {"$set": {"note": note}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Project notebook could not be update: {e}")
            return False

    @staticmethod
    def get_document_notebook(document_id) -> str:
        """
        Retrieve the notebook content for a given document.

        :param document_id: Document identifier.
        :type document_id: str

        :return: Notebook content as a string, empty string if not found.
        :rtype: str
        """
        try:
            with mongo_connection() as db:
                document = db.documents.find_one({"_id": ObjectId(document_id)})
                if document is None:
                    return ""
                return document.get("note", "")
        except Exception as e:
            print(f"Error retrieving document notebook: {e}")
            return ""

    @staticmethod
    def update_document_notebook(document_id, note) -> bool:
        """
        Update the notebook content for a document.

        :param document_id: Document identifier.
        :type document_id: str
        :param note: New notebook content.
        :type note: str

        :return: True if update was successful, else False.
        :rtype: bool
        """
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"note": note}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Document notebook could not be update: {e}")
            return False


