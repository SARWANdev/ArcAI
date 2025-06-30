from database.repository.user_repository import User as UserRepository
from model.user_profile.user import User as UserModel
from model.user_profile.view_mode import ViewMode
from database.repository.library_repository import Library as LibraryRepository
from model.document_reader.library import Library as LibraryModel

class UserService:
    def __init__(self):
        self.user_repository = UserRepository

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
        
    def deactivate_user(self, user_id):
        # Deactivates a user's account. Returns the result of the operation 
        return self.user_repository.deactivate_user(user_id)

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
        
