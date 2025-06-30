from services.user_management.user_service import UserService
from services.user_management.authentication_service import AuthenticationService

from flask import Blueprint

authenticate = Blueprint("authenticate", __name__)

class UserController:
    def __init__(self):
        self.user_service = UserService()
        self.auth_service = AuthenticationService()

    def login(self):
        return self.auth_service.login()

    def callback(self):
        return self.auth_service.callback()

    def logout(self):
        return self.auth_service.logout()

    def get_user_profile(self, user_id):
        pass

    def update_user_profile(self, user_id, first_name=None, last_name=None, email=None):
        pass

    def update_preferred_mode(self, user_id, mode):
        pass

    def get_user_projects(self, user_id):
        pass
