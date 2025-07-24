import os
from authlib.integrations.flask_client import OAuth
from database.repository.user_repository import UserRepository as UserRepository
from flask import url_for, session, redirect, jsonify

from model.user_profile.user import User
from dotenv import load_dotenv

load_dotenv()

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")


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
            sub_id = session["user"]["userinfo"]["sub"][14:]
            first_name = session["user"]["userinfo"]["given_name"]
            last_name = session["user"]["userinfo"]["family_name"]
            email = session["user"]["userinfo"]["email"]
            # Through UserRepository we will check if the user is already present in db
            try:
                #user = UserRepository(first_name=first_name, last_name=last_name, email=email, sub_id=sub_id)
                #user.new_user()
                new_user = User(user_id=sub_id, first_name=first_name, last_name=last_name, email=email)
                self.user_repository.save(new_user)

            except Exception as e:
                print(e) # Shows that the user already exists
            finally:
                UserRepository.activate_user(sub_id)
                return redirect(f"{frontend_url}/home")
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # Endpoint to get information about the user: name, picture, sub and user-verification
    def get_user_verification(self):
        if "user" not in session:
            return jsonify({"user-verification": False}), 401
        return jsonify({"user-verification": True,
                        "sub" : session["user"]["userinfo"]["sub"],
                        "picture" : session["user"]["userinfo"]["picture"],
                        "name" : session["user"]["userinfo"]["given_name"],
                        "userPreference" : self.user_repository.get_view_mode(session["user"]["userinfo"]["sub"][14:])}), 200

    # Endpoint to clear the session and redirect the user back to login page
    @staticmethod
    def logout():
        session.clear()
        return redirect(frontend_url)
