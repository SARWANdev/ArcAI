from services.library_service import LibraryService
from services.project_service import ProjectService
from services.document_service import DocumentService
from flask import Blueprint, Flask, jsonify, request

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

    def get_user_projects(self):
        try:
            # Get parameters from query string
            user_id = request.args.get("user_id")
            sort_by = request.args.get("sort_by", "title")  # default to 'title'
            order = request.args.get("order", "asc")  # default to 'asc'

            # Map frontend field names to database columns
            if sort_by == "Title":
                sort_by = "name"
            elif sort_by == "CreatedAt":
                sort_by = "created"
            elif sort_by == "LastUpdated":
                sort_by = "updated"

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            # Get sorted projects from service layer
            project_model_list = self.library_service.sort_library(user_id, sort_by, order)

            # Convert models to dictionaries for frontend
            project_list = [
                {
                    "Title": model.project_name,
                    "CreatedAt": model.created_at,
                    "LastUpdated": model.updated_at
                    # Add other fields if needed
                }
                for model in project_model_list
            ]

            # Return both success message AND the project data
            return jsonify({
                "status": "success",
                "message": "Projects retrieved successfully",
                "data": {
                    "projects": project_list,
                    "sort_by": sort_by,
                    "order": order
                }
            }), 200

        except Exception as e:
            print(f"Error in get_user_projects: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to retrieve projects",
                "error": str(e)
            }), 500

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
        self.library.add_url_rule("/library/get-projects", view_func=self.get_user_projects)
        app.register_blueprint(self.library)

