import os
from authlib.integrations.flask_client import OAuth
from database.repository.user_repository import User as UserRepository
from flask import url_for, session, redirect, jsonify

class AuthenticationService:
    def __init__(self):
        self.user_repository = UserRepository
        self.oauth = OAuth()

    def init_oauth(self, app):
        env = os.environ
        self.oauth.init_app(app)
        self.oauth.register(
            name="auth0",
            client_id=env.get("AUTH0_CLIENT_ID"),
            client_secret=env.get("AUTH0_CLIENT_SECRET"),
            client_kwargs={"scope": "openid profile email"},
            server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
        )

    def login(self):
        # FIX: This url_for blueprint name should match the blueprint name in user_controller.py, i.e., "authenticate"
        return self.oauth.auth0.authorize_redirect(
            redirect_uri=url_for("authenticate.callback", _external=True),
            prompt="login"
        )

    def callback(self):
        try:
            token = self.oauth.auth0.authorize_access_token()
            session["user"] = token
            return redirect("http://localhost:5173/home")
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def logout(self):
        session.clear()
        return redirect("http://localhost:5173")
