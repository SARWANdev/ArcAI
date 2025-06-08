from database.repository.user_repository import User as UserRepository

class AuthenticationService:
    def __init__(self):
        self.user_repository = UserRepository

    def authenticate_user(self, email, password):
        pass

    def generate_auth_token(self, user_id):
        pass

    def validate_auth_token(self, token):
        pass

    def hash_password(self, password):
        pass

    def verify_password(self, hashed_password, plain_password):
        pass

    def create_session(self, user_id):
        pass

    def invalidate_session(self, session_id):
        pass

    def refresh_token(self, refresh_token):
        pass

    def validate_session(self, session_id):
        pass
