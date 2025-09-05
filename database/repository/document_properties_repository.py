from bson import ObjectId

from database.repository.document_repository import DocumentRepository
from database.repository.pdf_master_repository import PdfMasterRepository
from database.repository.project_repository import ProjectRepository
from database.utils.mongo_connector import mongo_connection
from exceptions.tag_exceptions import InvalidTagName, MissingTagColor

class DocumentPropertiesRepository:

    @staticmethod
    def mark_as_favorite(document_id) -> bool:
        """
        Marks a document as favorite in the database.

        :param document_id: The ID of the document to mark as favorite.

        :return: True if the update was successful, False otherwise.
        :rtype: bool
        """
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"favorite": True}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Document could not be mark as favorite: {e}")
            return False


    @staticmethod
    def mark_as_not_favorite(document_id) -> bool:
        """
        Marks a document as not favorite in the database.

        :param document_id:  The ID of the document to mark as not favorite.

        :return: True if the update was successful, False otherwise.        
        :rtype: bool
        """
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"favorite": False}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Document could not be mark as not favorite: {e}")
            return False

    @staticmethod
    def mark_as_read(document_id):
        """
        Marks a document as read in the database.

        :param document_id: The ID of the document to mark as read.

        :return: The ID of the document was marked as read.
        """
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"read": True}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Document could not be mark as read: {e}")
            return False

    @staticmethod
    def mark_as_not_read(document_id) -> bool:
        """
        Marks a document as not read in the database.

        :param document_id: The ID of the document to mark as not read.

        :return: True if the update was successful, False otherwise.
        :rtype: bool
        """
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"read": False}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Document could not be mark as read: {e}")
            return False

    @staticmethod
    def update_journal(document_id, journal_name) -> bool:
        """
        Updates a journal document in the database.

        :param document_id: The ID of the document to update.
        :param journal_name: 

        :return:
        """
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"journal": journal_name}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Journal name could not be update: {e}")
            return False

    @staticmethod
    def update_tag(document_id, tag_name) -> bool:
        """
        Updates the tag name for a document in the database.

        :param document_id: The ID of the document to update.
        :type document_id: str
        :param tag_name: The new tag name to set for the document.
        :type tag_name: str

        :returns: True if the update was successful, False otherwise.
        :rtype: bool
        :raises InvalidTagName: If the tag name is invalid
        """
        # Validate tag name if provided (None is allowed for removing tags)
        if tag_name is not None:
            if not isinstance(tag_name, str):
                raise InvalidTagName("Tag name must be a string")
            
            tag_name = tag_name.strip()
            if len(tag_name) < InvalidTagName.MIN_NAME_LENGTH:
                raise InvalidTagName(f"Tag name must be at least {InvalidTagName.MIN_NAME_LENGTH} character long")
            
            if len(tag_name) > InvalidTagName.MAX_NAME_LENGTH:
                raise InvalidTagName(f"Tag name cannot exceed {InvalidTagName.MAX_NAME_LENGTH} characters")
        
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"tag_name": tag_name}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Tag name could not be update: {e}")
            return False

    @staticmethod
    def update_tag_color(document_id, tag_color) -> bool:
        """
        Updates the tag color for a document in the database.

        :param document_id: The ID of the document to update.
        :type document_id: str
        :param tag_color: The new tag color to set for the document.
        :type tag_color: str

        :returns: True if the update was successful, False otherwise.
        :rtype: bool
        :raises MissingTagColor: If the tag color is missing or invalid
        """
        # Validate tag color if provided (None is allowed for removing tags)
        if tag_color is not None:
            if not isinstance(tag_color, str):
                raise MissingTagColor("Tag color must be a string")
            
            tag_color = tag_color.strip()
            if not tag_color:
                raise MissingTagColor("Tag color cannot be empty")
        
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"tag_color": tag_color}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Tag color could not be update: {e}")
            return False

    @staticmethod
    def set_new_project_id(document_id, new_project_id) -> bool:
        """
        Updates the project ID associated with a document.

        :param document_id: The ID of the document to update.
        :type document_id: str
        :param new_project_id: The new project ID to assign to the document.
        :type new_project_id: str

        :returns: True if the update was successful, False otherwise.
        :rtype: bool
        """
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"project_id": new_project_id}})
                return result.modified_count > 0
        except Exception as e:
            print(f"New project id could not be set: {e}")
            return False

    @staticmethod
    def get_project_id(document_id):
        """
        Retrieves the project ID associated with a document.

        :param document_id: The ID of the document.
        :type document_id: str

        :returns: The project ID if found, otherwise an empty string.
        :rtype: str
        """
        try:
            with mongo_connection() as db:
                project_id = db.documents.find_one({"_id": ObjectId(document_id)}, {"project_id": 1}).get("project_id")
                return project_id
        except Exception as e:
            print(f"Project id could not be found: {e}")
            return ""

    @staticmethod
    def get_first_author(document_id):
        """
        Updates the project ID associated with a document.

        :param document_id: The ID of the document to update.
        :type document_id: str
        :param new_project_id: The new project ID to assign to the document.
        :type new_project_id: str

        :returns: True if the update was successful, False otherwise.
        :rtype: bool
        """
        pdf_master_id = DocumentRepository.get_pdf_master_id(document_id)
        return PdfMasterRepository.get_first_author(pdf_master_id)

    @staticmethod
    def get_project_id_and_name(document_id: str) -> tuple[str, str]:
        """
        Retrieves the project name and project id associated with a document.
        :param document_id:  The ID of the document to update.
        :return: A tuple wit the project name and the project ID.
        """

        project_id = DocumentPropertiesRepository.get_project_id(document_id)
        if not project_id:
            return "", ""
        project_name = ProjectRepository.get_project_name(project_id)
        return project_id, project_name
