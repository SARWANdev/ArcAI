from services.library_service import LibraryService
from services.project_service import ProjectService
from services.document_service import DocumentService
from flask import Blueprint, Flask, jsonify, request


# Changed
class LibraryController:
    def __init__(self, app : Flask):
        self.library_service = LibraryService()
        self.project_service = ProjectService()
        # The line below is causing error
        self.document_service = DocumentService()
        # To create routes for library related method's endpoints
        self.library = Blueprint('library', __name__)
        # To register these routes in the flask application
        self.register_library_routes(app)

    def get_embeddings(self, item_ids=None):
        pass

    def get_project(self, project_id):
        pass

    def search_documents(self, query, filters=None):
        pass

    # New function
    def create_project(self):
        try:
            data = request.get_json()

            user_id = data.get("user_id")
            name = data.get("name")

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            # Call your service layer
            self.project_service.create_project(user_id, name)

            return jsonify({"success": "A project has been created"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def download_project(self, project_id):
       pass

    def delete_project(self, project_id):
        pass

    def rename_project(self, project_id, name):
        pass

    def sort_projects(self, sort_by, sort_order):
        pass

    def filter_projects(self, filters):
        pass

    def get_item_metadata(self, item_id, item_type):
        pass

    # To register all the library-routes
    def register_library_routes(self, app):
        self.library.add_url_rule("/library/create-project", view_func=self.create_project, methods=["POST"])
        app.register_blueprint(self.library)

