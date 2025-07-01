import os
from authlib.integrations.flask_client import OAuth
from database.repository.user_repository import User as UserRepository
from flask import url_for, session, redirect, jsonify


class AuthenticationService:
    def __init__(self, app):
        self.user_repository = UserRepository
        self.oauth = OAuth(app)

    # To initialize Auth0
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
    # Endpoint to redirect user to the login page of the auth0
    def login(self):
        return self.oauth.auth0.authorize_redirect(
            redirect_uri=url_for("authenticate.callback", _external=True),
            prompt="login"
        )

    # Endpoint to redirect user to home page if a success or raises an error
    def callback(self):
        try:
            token = self.oauth.auth0.authorize_access_token()
            session["user"] = token
            return redirect("http://localhost:5173/home")
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # Endpoint to get information about the user: name, picture, sub and user-verification
    @staticmethod
    def get_user_verification():
        if "user" not in session:
            return jsonify({"user-verification": False}), 401
        return jsonify({"user-verification": True,
                        "sub" : session["user"]["userinfo"]["sub"],
                        "picture" : session["user"]["userinfo"]["picture"],
                        "name" : session["user"]["userinfo"]["given_name"]}), 200

    # Endpoint to clear the session and redirect the user back to login page
    @staticmethod
    def logout():
        session.clear()
        return redirect("http://localhost:5173")
