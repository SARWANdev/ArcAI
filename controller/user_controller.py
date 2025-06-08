from services.authentication_service import UserService
from services.authentication_service import AuthenticationService

class UserController:
    def __init__(self):
        self.user_service = UserService()
        self.auth_service = AuthenticationService()


    def login(self, email, password):
        pass

    def logout(self, user_id):
        pass

    def get_user_profile(self, user_id):
        pass

    def update_user_profile(self, user_id, first_name=None, last_name=None, email=None):
        pass

    def update_preferred_mode(self, user_id, mode):
        pass

    def get_user_projects(self, user_id):
        pass
