import os
from authlib.integrations.flask_client import OAuth
from database.repository.user_repository import UserRepository as UserRepository
from flask import url_for, session, redirect, jsonify

from model.user_profile.user import User
from dotenv import load_dotenv

load_dotenv()
 
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")


class AuthenticationService:
    """
    Service for handling user authentication using Auth0 and session management.

    This service provides methods to initialize OAuth, handle login and logout,
    process authentication callbacks, and verify user sessions.
    """
    def __init__(self, app):
        """
        Initialize the AuthenticationService.

        :param app: The Flask application instance.
        :type app: Flask
        """
        self.user_repository = UserRepository
        self.oauth = OAuth(app)

    def init_oauth(self, app):
        """
        Initialize OAuth with Auth0 configuration.

        :param app: The Flask application instance.
        :type app: Flask
        """
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
        """
        Redirect the user to the Auth0 login page.

        :return: A redirect response to the Auth0 login page.
        """
        return self.oauth.auth0.authorize_redirect(
            redirect_uri=url_for("authenticate.callback", _external=True),
            prompt="login"
        )

    def callback(self):
        """
        Handle the Auth0 callback after user authentication.

        Retrieves user information from Auth0, saves the user if new, activates the user,
        and redirects to the frontend home page. Returns an error response if authentication fails.

        :return: A redirect response to the frontend home page or an error response.
        """
        try:
            token = self.oauth.auth0.authorize_access_token()
            session["user"] = token
            sub_id = session["user"]["userinfo"]["sub"][14:]
            first_name = session["user"]["userinfo"]["given_name"]
            last_name = session["user"]["userinfo"]["family_name"]
            email = session["user"]["userinfo"]["email"]
            try:
                new_user = User(user_id=sub_id, first_name=first_name, last_name=last_name, email=email)
                self.user_repository.save(new_user)
            except Exception as e:
                print(e)  # User may already exist
            finally:
                UserRepository.activate_user(sub_id)
                return redirect(f"{frontend_url}/home")
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def get_user_verification(self):
        """
        Get information about the current user and verify session.

        :return: A JSON response with user verification status and user info.
        :rtype: flask.Response
        """
        if "user" not in session:
            return jsonify({"user-verification": False}), 401
        return jsonify({
            "user-verification": True,
            "sub": session["user"]["userinfo"]["sub"],
            "picture": session["user"]["userinfo"]["picture"],
            "name": session["user"]["userinfo"]["given_name"],
            "userPreference": self.user_repository.get_view_mode(session["user"]["userinfo"]["sub"][14:])
        }), 200

    @staticmethod
    def logout():
        """
        Log out the current user by clearing the session and redirecting to the login page.

        :return: A redirect response to the frontend login page.
        """
        session.clear()
        return redirect(frontend_url)
