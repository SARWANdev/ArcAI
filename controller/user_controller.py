from bson import ObjectId

from services.user_management.user_service import UserService
from services.user_management.authentication_service import AuthenticationService
from flask import Blueprint, Flask, request, jsonify


class UserController:
    def __init__(self, auth_service: AuthenticationService, app : Flask):
        self.user_service = UserService()
        self.auth_service = auth_service
        self.authenticate = Blueprint("authenticate", __name__)
        self.register_auth_routes(app)

    def login(self):
        return self.auth_service.login()

    def callback(self):
        return self.auth_service.callback()

    def logout(self):
        return self.auth_service.logout()

    def get_user_verification(self):
        return self.auth_service.get_user_verification()

    def update_preferred_mode(self):
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            mode = data.get("mode")
            value = False
            if not user_id or not mode:
                return jsonify({"error": "Missing user_id or mode"}), 400

            if mode == "light":
                value = True

            self.user_service.update_preference(user_id=user_id, value = value)

            # --- Database logic to move the document ---
            # For example:

            return jsonify({"message": "Update mode successfully"}), 200

        except Exception as e:
            print(f"Error in update_preferred_mode: {e}")
            return jsonify({"error": "Internal server error"}), 500

    def delete_account(self):
        try:
            data = request.get_json()  # Parse JSON body
            user_id = data.get("user_id")
            if not user_id:
                return {"error": "user_id missing"}, 400

            self.user_service.remove_user(user_id)

            # Optionally log the user out
            self.auth_service.logout()

            return jsonify({"message": "Account deleted successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def register_auth_routes(self, app):
        self.authenticate.add_url_rule("/login", view_func=self.login)
        self.authenticate.add_url_rule("/callback", view_func=self.callback)
        self.authenticate.add_url_rule("/logout", view_func=self.logout)
        self.authenticate.add_url_rule("/user-info", view_func=self.get_user_verification)
        self.authenticate.add_url_rule("/user/delete", view_func=self.delete_account, methods=["DELETE"])
        app.add_url_rule("/user/toggle", view_func=self.update_preferred_mode, methods=['POST'])
        app.register_blueprint(self.authenticate)