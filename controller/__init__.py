import os

from flask import Flask
from dotenv import find_dotenv, load_dotenv
from os import environ as env
from flask_cors import CORS

import library_controller
from controller.chat_controller import ChatController
from controller.project_controller import ProjectController
from services.user_management.authentication_service import AuthenticationService
from controller.user_controller import UserController
from controller.library_controller import LibraryController
from controller.document_controller import DocumentController

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
user_controller = UserController(authentication_service, app)
library_controller = LibraryController(app)
project_controller = ProjectController(app)
chat_controller = ChatController(app)
document_controller = DocumentController(app)

# Run the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(env.get("PORT", 3000)))