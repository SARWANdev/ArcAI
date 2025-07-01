from services.user_management.user_service import UserService
from services.user_management.authentication_service import AuthenticationService
from flask import Blueprint
class UserController:
    def __init__(self, auth_service: AuthenticationService):
        self.user_service = UserService()
        self.auth_service = auth_service
        self.authenticate = Blueprint("authenticate", __name__)

    def login(self):
        return self.auth_service.login()

    def callback(self):
        return self.auth_service.callback()

    def logout(self):
        return self.auth_service.logout()

    def get_user_verification(self):
        return self.auth_service.get_user_verification()

    def get_user_profile(self, user_id):
        pass

    def update_user_profile(self, user_id, first_name=None, last_name=None, email=None):
        pass

    def update_preferred_mode(self, user_id, mode):
        pass

    def get_user_projects(self, user_id):
        pass

    # To register all the auth-routes
    def register_auth_routes(self, app):
        controller = UserController(self.auth_service)
        self.authenticate.add_url_rule("/login", view_func=controller.login)
        self.authenticate.add_url_rule("/callback", view_func=controller.callback)
        self.authenticate.add_url_rule("/logout", view_func=controller.logout)
        self.authenticate.add_url_rule("/user-info", view_func=controller.get_user_verification)
        # To register the blueprint in the application variable
        app.register_blueprint(self.authenticate)
