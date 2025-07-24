import os
import posixpath

from dotenv import load_dotenv

from database.repository.user_repository import UserRepository as UserRepository
from model.user_profile.user import User as UserModel

from database.repository.library_repository import Library as LibraryRepository
from services.conversation_service import ConversationService
from services.project_service import ProjectService
from services.upload_manager.server_conection import delete_remote_directory


load_dotenv()
remote_dir = os.getenv("REMOTE_DIR")


class UserService:
    """
    Service class for user-related operations, including profile retrieval, removal,
    and user preferences management.

    Responsibilities
    ================
    - Retrieve user profiles
    - Remove users and associated data
    - Get and update user preferences (e.g., view mode)
    """
    def __init__(self):
        """
        Initialize the UserService with required repositories and services.
        """
        self.user_repository = UserRepository
        self.project_service = ProjectService()
        self.conversation_service = ConversationService()

    def get_user_profile(self, user_id):
        """
        Retrieve a user profile by user ID.

        :param user_id: The ID of the user.
        :type user_id: str
        :returns: User model object or None if not found.
        :rtype: UserModel | None
        """
        user_data = self.user_repository.get_user_by_id(user_id)
        if not user_data:
            return None
        user_model = UserModel.from_dict(user_data)
        return user_model

    def remove_user(self, user_id):
        """
        Remove a user from the database, delete all their documents on the server,
        and deactivate the user.

        :param user_id: The ID of the user to remove.
        :type user_id: str
        :returns: None
        """
        project_ids = LibraryRepository.get_user_library(user_id)

        for project_id in project_ids:
            project_id = str(project_id.get('_id'))
            self.project_service.delete_project(project_id)

        user_path = posixpath.join(remote_dir, user_id)
        delete_remote_directory(user_path)
        self.user_repository.deactivate_user(user_id)
        self.conversation_service.delete_all_converstations(user_id)

    def get_preference(self, user_id):
        """
        Get the user's view mode preference.

        :param user_id: The ID of the user.
        :type user_id: str
        :returns: The user's view mode preference (True for light mode, False for dark mode), or None if not found.
        :rtype: bool | None
        """
        user_data = self.user_repository.get_user_by_id(user_id)
        if not user_data:
            return None
        preference = user_data.get('view_mode')
        return preference

    def update_preference(self, user_id, value):
        """
        Update the user's view mode preference.

        :param user_id: The ID of the user.
        :type user_id: str
        :param value: The new view mode preference (True for light mode, False for dark mode).
        :type value: bool
        :returns: True if the update was successful, False otherwise.
        :rtype: bool
        """
        return self.user_repository.update_view_mode(user_id, value)

        
