from flask import Flask
from dotenv import find_dotenv, load_dotenv
from os import environ as env
from flask_cors import CORS
from services.user_management.authentication_service import AuthenticationService
from controller.user_controller import UserController

# Load environment variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Create Flask app
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])


# Initialize OAuth
authentication_service = AuthenticationService(app)
authentication_service.init_oauth(app)

# Initialize authentication routes
user_controller = UserController(authentication_service)
user_controller.register_auth_routes(app)

# Run the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(env.get("PORT", 3000)))