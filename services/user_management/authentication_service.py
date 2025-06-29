# '''Required Packages for authentication'''

# from os import environ as env
# from authlib.integrations.flask_client import OAuth
# from dotenv import find_dotenv, load_dotenv
# from flask import Flask
# from flask_cors import CORS
from database.repository.user_repository import User as UserRepository

class AuthenticationService:
    def __init__(self):
        self.user_repository = UserRepository

    # '''Template needed to load environment variables and run the flask application'''

    # # Load environment variables
    # ENV_FILE = find_dotenv()
    # if ENV_FILE:
    #     load_dotenv(ENV_FILE)
    #
    # app = Flask(__name__)
    # CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
    # app.secret_key = env.get("APP_SECRET_KEY")

    # '''Template given by Auth0 to run their authentication service'''

    # oauth = OAuth(app)
    # oauth.register(
    #     name="auth0",
    #     client_id=env.get("AUTH0_CLIENT_ID"),
    #     client_secret=env.get("AUTH0_CLIENT_SECRET"),
    #     client_kwargs={"scope": "openid profile email"},
    #     server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
    # )

    # --- Auth Routes ---

    # @app.route("/login")
    def login(self):
        pass
        # '''Redirects to Auth0 login page.'''

        # return oauth.auth0.authorize_redirect(
        #     redirect_uri=url_for("callback", _external=True),
        #     prompt="login"  # Force fresh login every time
        # )

    #

    # @app.route("/callback")
    def callback(self):
        pass
        # '''Auth0 redirects here after login.'''

        # try:
        #     # Fetch user token from Auth0
        #     token = oauth.auth0.authorize_access_token()
        #     session["user"] = token  # Store user in session
        #
        #     # Redirect to React's frontend with success flag
        #     frontend_redirect_url = "http://localhost:5173/home"
        #     return redirect(frontend_redirect_url)
        #
        # except Exception as e:
        #     return jsonify({"error": str(e)}), 400

    # @app.route("/logout")
    def logout(self):
        pass
        # '''Logs out user from Auth0 and clears session.'''

        # session.clear()
        #
        # # Auth0 logout URL (ends Auth0 session too)
        # return redirect(
        #     f"https://{env.get('AUTH0_DOMAIN')}/v2/logout?"
        #     + urlencode(
        #         {
        #             "returnTo": url_for("home", _external=True),
        #             "client_id": env.get("AUTH0_CLIENT_ID"),
        #             "federated": ""  # Optional: Log out from Google/etc.
        #         },
        #         quote_via=quote_plus,
        #     )
        # )

    # @app.route("/api/user")
    def get_user(self):
        pass
        # '''Returns current user data (for React to check auth status).'''

        # if "user" not in session:
        #     return jsonify({"error": "Unauthorized"}), 401
        # return jsonify(session["user"])

    # '''This is not needed here as the flask application will be run in another module but is kept here to show the reference to the code above'''

    # --- Run Server ---
    # if __name__ == "__main__":
    #     app.run(host="0.0.0.0", port=env.get("PORT", 3000))
