from database.repository.user_repository import User as UserRepository

class UserService:
    def __init__(self):
        self.user_repository = UserRepository

    def get_user_profile(self, user_id):
        # Fetch profile data from database
        pass

    def update_user_profile(self, user_id, first_name=None, last_name=None, email=None):
        # Update basic user information
        pass

    def get_preference(self, user_id):
        # Return user preferences (e.g., UI mode)
        pass

    def update_preference(self, user_id, preference_key, value):
        # Update a user preference like dark/light mode
        pass

    def get_user_projects(self, user_id):
        # Return list of projects associated with this user
        pass

    def get_user_library(self, user_id):
        #return the user's library
        pass

    
