from flask import Blueprint, redirect, session, url_for, jsonify
from flask.views import MethodView
from authlib.integrations.flask_client import OAuth
from os import environ as env
import requests
routes = Blueprint("routes", __name__)
oauth = OAuth()

# -- Initialize OAuth Auth0 --
def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name="auth0",
        client_id=env.get("AUTH0_CLIENT_ID"),
        client_secret=env.get("AUTH0_CLIENT_SECRET"),
        client_kwargs={"scope": "openid profile email"},
        server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
    )

# --- Auth Controller ---

class LoginController(MethodView):
    def get(self):
        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for("routes.callback", _external=True),
            prompt="login"
        )

class CallbackController(MethodView):
    def get(self):
        try:
            token = oauth.auth0.authorize_access_token()
            session["user"] = token
            return redirect("http://localhost:5173/home")
        except Exception as e:
            return jsonify({"error": str(e)}), 400

class LogoutController(MethodView):
    def get(self):
        session.clear()
        return redirect("http://localhost:5173")

# --- User Controller ---

class UserController(MethodView):
    def get(self):
        if "user" not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return jsonify(session["user"])

# --- Register routes to Blueprint ---

routes.add_url_rule("/login", view_func=LoginController.as_view("login"))
routes.add_url_rule("/callback", view_func=CallbackController.as_view("callback"))
routes.add_url_rule("/logout", view_func=LogoutController.as_view("logout"))
routes.add_url_rule("/api/user", view_func=UserController.as_view("get_user"))