from flask import Flask
from dotenv import find_dotenv, load_dotenv
from os import environ as env
from flask_cors import CORS
from services.user_management.authentication_service import AuthenticationService
from user_controller import authenticate, UserController

# Load .env
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Create Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
app.secret_key = env.get("APP_SECRET_KEY")

authentication_service = AuthenticationService()
authentication_service.init_oauth(app)

app.register_blueprint(authenticate)

controller = UserController()
authenticate.add_url_rule("/login", view_func=controller.login)
authenticate.add_url_rule("/callback", view_func=controller.callback)
authenticate.add_url_rule("/logout", view_func=controller.logout)

# Run the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(env.get("PORT", 3000)))