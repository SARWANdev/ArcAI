from flask import Flask
from dotenv import find_dotenv, load_dotenv
from os import environ as env
from flask_cors import CORS

from routes import routes, init_oauth  # Import from routes.py

# Load .env
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Create Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
app.secret_key = env.get("APP_SECRET_KEY")

# Init OAuth and register blueprint
init_oauth(app)
app.register_blueprint(routes)

# Run the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(env.get("PORT", 3000)))