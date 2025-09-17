import pymongo
import pymongo.errors

from database.repository.date_time_utils import get_utc_zulu_timestamp
from database.utils.mongo_connector import mongo_connection
from model.document_reader.project import Project 
from bson import ObjectId




class ProjectRepository:
    """
    Repository class for handling Project-related database operations.

    Provides static methods to save, retrieve, update, and delete projects in the MongoDB database.
    """
    
    @staticmethod
    def save(project: Project) -> str:
        """
        Save a new project to the database.

        :param project: Project instance to be saved.
        :type project: Project

        :return: The ID of the inserted project as a string, or an empty string if duplicate.
        :rtype: str
        """
        with mongo_connection() as db:
            try:
                result = db.projects.insert_one(project.new_project_dict())
                project_id = str(result.inserted_id)
                return project_id
            except pymongo.errors.DuplicateKeyError:
                print(f"Project with name '{project.new_project_dict().get('project_name')}' already exists")
                return ""
    
    @staticmethod
    def get_note(project_id):
        """
        Retrieve the note field from a project by its ID.

        :param project_id: The ID of the project.
        :type project_id: str or ObjectId

        :return: The note as a string, or an empty string if not found or error occurs.
        :rtype: str
        """
        try:
            with mongo_connection() as db:
                result = db.projects.find_one({"_id": ObjectId(project_id)}, {"note": 1}).get("note")
                return str(result)
        except Exception as e:
            print(f"System can not return note from project {e}")
            return ""

    @staticmethod
    def get_project_by_id(project_id: str) -> dict:
        """
        Retrieve a project by its ID.

        :param project_id: The ID of the project.
        :type project_id: str or ObjectId

        :return: The project document as a dictionary.
        :rtype: dict

        :raises Exception: If a database error occurs.
        """
        try:
            with mongo_connection() as db:
                # Convert to ObjectId if it's a string
                if isinstance(project_id, str):
                    project_id = ObjectId(project_id)
                return db.projects.find_one({"_id": ObjectId(project_id)})
        except Exception as e:
            print(e)
            raise

    @staticmethod
    def get_project_by_name(project_name: str) -> dict:
        """
        Retrieve a project by its name.

        :param project_name: The name of the project.
        :type project_name: str

        :return: The project document as a dictionary.
        :rtype: dict

        :raises Exception: If a database error occurs.
        """
        try:
            with mongo_connection() as db:
                return db.projects.find_one({"project_name": project_name})
        except Exception as e:
            print(f"Error getting project by name: {str(e)}")
            raise

    @staticmethod
    def update_name(project_id, new_name) -> bool:
        """
        Update the name of a project.

        :param project_id: The ID of the project to update.
        :type project_id: str or ObjectId
        :param new_name: The new name for the project.
        :type new_name: str

        :return: True if the project name was updated, False otherwise.
        :rtype: bool
        """
        try:
            with mongo_connection() as db:
                result = db.projects.update_one({"_id": ObjectId(project_id) }, {"$set": {"project_name": new_name,
                                                                      "updated_at": get_utc_zulu_timestamp()}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Project name could not be update: {e}")
            return False

    @staticmethod
    def delete_project(project_id) -> bool:
        """
        Delete a project by its ID.

        :param project_id: The ID of the project to delete.
        :type project_id: str or ObjectId

        :return: True if the project was deleted, False otherwise.
        :rtype: bool
        """
        try:
            with mongo_connection() as db:
                # Ensure project_id is ObjectId
                if isinstance(project_id, str):
                    project_id = ObjectId(project_id)
                result = db.projects.delete_one({"_id": project_id})
                return result.deleted_count > 0
        except Exception as e:
            print(f"Project could not be deleted: {e}")
            return False
        
    @staticmethod
    def get_user_id(project_id) -> str:
        """
        Retrieve the user ID associated with a project.

        :param project_id: The ID of the project.
        :type project_id: str or ObjectId
        
        :return: The user ID as a string, or an empty string if not found or error occurs.
        :rtype: str
        """
        try:
            with mongo_connection() as db:
                return db.projects.find_one({"_id": ObjectId(project_id)},{"user_id": 1}).get("user_id")
        except Exception as e:
            print(f"Error getting user id from project {e}")
            return str()

    @staticmethod
    def get_project_name(project_id) -> str:
        try:
            with mongo_connection() as db:
                return db.projects.find_one({"_id": ObjectId(project_id)}, {"project_name": 1}).get("project_name")
        except Exception as e:
            print(f"Error getting project name from project {e}")
            return str()

    @staticmethod
    def project_exists(project_id) -> bool:
        try:
            with mongo_connection() as db:
                result = db.projects.find_one({"_id": ObjectId(project_id)})
                return result is not None
        except Exception as e:
            print(f"Project could not be retrieved: {e}")
            return False




