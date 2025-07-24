import os
import posixpath

from dotenv import load_dotenv

from database.repository.user_repository import User as UserRepository
from model.user_profile.user import User as UserModel
from model.user_profile.view_mode import ViewMode
from database.repository.library_repository import Library as LibraryRepository, Library
from model.document_reader.library import Library as LibraryModel
from services.project_service import ProjectService
from services.upload_manager.server_conection import delete_remote_directory
from services.user_management.authentication_service import AuthenticationService

load_dotenv()
remote_dir = os.getenv("REMOTE_DIR")


class UserService:
    def __init__(self):
        self.user_repository = UserRepository
        self.project_service = ProjectService()

    def get_user_profile(self, user_id):
        #Fetch user data from DB
        user_data = UserRepository.get_user_by_id(user_id)
        if not user_data:
            return None
        # Map DB fields to UserModel
        user_model = UserModel(
            user_id = user_data.get('user_id'),
            first_name = user_data.get('first_name'),
            last_name = user_data.get('last_name'),
            email = user_data.get('email')
        )
        user_model.prefered_mode = user_data.get('preferred_mode')
        return user_model
        
    def delete_user_contents(self, user_id):
        # Deactivates a user's account. Returns the result of the operation 
        return self.user_repository.deactivate_user(user_id)

    def remove_user(self, user_id):
        """
        1. delete all documents in each folder
        2. delete all projects in each folder
        3. delete all empty folders

        last step: deactivate user account if the rest was succesful
        :param user_id:
        :return:
        """

        #get all project_ids as strings
        project_ids = Library.get_user_library(user_id)

        for project_id  in project_ids:
            project_id = str(project_id.get('_id'))
            self.project_service.delete_project(project_id)

        user_path =  posixpath.join(remote_dir, user_id)
        delete_remote_directory(user_path)
        self.delete_user_contents(user_id)

        #put or call the logout function



    def get_preference(self, user_id):
        # Return user preferences (e.g., UI mode)
        user_data = UserRepository.get_user_by_id(user_id)
        if not user_data:
            return None
        preference = user_data.get('preferred_mode')
        return preference

    def update_preference(self, user_id, value):
        # Update a user preference like dark/light mode
        result = self.user_repository.update_view_mode(user_id, value)
        return result == 1
        

    def get_user_library(self, user_id):
        #return the user's library
        library_data = LibraryRepository.get_user_library(user_id)
        if not library_data:
            return None
        library_model = LibraryModel()
        return library_data
        #TODO: convert all objects into model classes
        
