from database.repository.user_repository import User as UserRepository
from model.user_profile.user import User as UserModel

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
            user_id=user_data.get('user_id'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email')
        )
        user_model.prefered_mode = user_data.get('preferred_mode')
        return user_model
        
        

    def update_user_profile(self, user_id, first_name=None, last_name=None, email=None):
        # Update basic user information
        pass

    def get_preference(self, user_id):
        # Return user preferences (e.g., UI mode)
        user_data = UserRepository.get_user_by_id(user_id)
        if not user_data:
            return None
        preference = user_data.get('preferred_mode')
        return preference

    def update_preference(self, user_id, preference_key, value):
        # Update a user preference like dark/light mode
        pass

    def get_user_projects(self, user_id):
        # Return list of projects associated with this user
        pass

    def get_user_library(self, user_id):
        #return the user's library
        pass

    
