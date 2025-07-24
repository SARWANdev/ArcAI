import os
import posixpath

from dotenv import load_dotenv

from database.repository.user_repository import UserRepository as UserRepository
from model.user_profile.user import User as UserModel, User

from database.repository.library_repository import Library as LibraryRepository, Library
from model.document_reader.library import Library as LibraryModel
from services.conversation_service import ConversationService
from services.project_service import ProjectService
from services.upload_manager.server_conection import delete_remote_directory


load_dotenv()
remote_dir = os.getenv("REMOTE_DIR")


class UserService:
    def __init__(self):
        self.user_repository = UserRepository
        self.project_service = ProjectService()
        self.conversation_service = ConversationService()

    def get_user_profile(self, user_id):
        """
        Get user model Object by user_id.

        :param user_id: The id of the user.
        :return: User model Object.
        """
        user_data = self.user_repository.get_user_by_id(user_id)
        if not user_data:
            return None
        user_model = User.from_dict(user_data)
        return user_model


    def remove_user(self, user_id):
        """
        this method removes a user from the database and deletes all its documents in the server
        as well switches off the bool variable active to false

        :param user_id: is the id of the user
        """
        project_ids = Library.get_user_library(user_id)

        for project_id  in project_ids:
            project_id = str(project_id.get('_id'))
            self.project_service.delete_project(project_id)

        user_path =  posixpath.join(remote_dir, user_id)
        delete_remote_directory(user_path)
        self.user_repository.deactivate_user(user_id)
        self.conversation_service.delete_all_converstations(user_id)




    def get_preference(self, user_id):
        """
        this method returns the preference of the user
        :param user_id: the id of the user
        :return: a bool, True is light mode and False is dark mode
        """
        user_data = self.user_repository.get_user_by_id(user_id)
        if not user_data:
            return None
        preference = user_data.get('view_mode')
        return preference

    def update_preference(self, user_id, value):
        """
        this method updates the preference of the user either to dark of light mode

        :param user_id: the id of the user
        :param value: True is light mode and False is dark mode
        :return: True if update was successful, False otherwise
        """
        return self.user_repository.update_view_mode(user_id, value)

        
