from bson import ObjectId

from services.project_service import ProjectService
from services.document_service import DocumentService
from flask import Blueprint, Flask, jsonify, request

class ProjectController:
    def __init__(self, app : Flask):
        self.project_service = ProjectService()
        self.document_service = DocumentService()
        # To create routes for project related method's endpoints
        self.project = Blueprint('project', __name__)
        self.register_project_routes(app)

    def get_user_projects(self, user_id):
        pass

    def update_project(self, project_id, name=None, description=None, note=None):
        pass

    def get_document(self, document_id):
        pass

    def duplicate_document(self, project_id, document_id):
        pass

    def delete_document(self, document_id):
        pass

    def upload_document(self, project_id, file_path, name=None):
        pass

    def download_document(self, document_id):
        pass

    def rename_document(self, document_id, name):
        pass

    def get_project_documents(self):
        try:
            # Get parameters from query string
            user_id = request.args.get("user_id")
            project_id = ObjectId(request.args.get("project_id"))


            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            documents = self.document_service.get_project_documents(project_id)
            print(documents)
            print(f"The user {user_id} wants document from the project {project_id}")

            # Return both success message AND the project data
            return jsonify({
                "status": "success",
                "message": "Documents retrieved successfully",
            }), 200

        except Exception as e:
            print(f"Error to get projects from documents: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to retrieve projects",
                "error": str(e)
            }), 500

    def get_project_embeddings(self, project_id, document_ids=None):
        pass

    def move_documents(self, item_id, destination_id):
        pass

    def sort_project_documents(self, project_id, sort_by, sort_order):
        pass

    def filter_project_documents(self, project_id, filters):
        pass

    def search_project_documents(self, project_id, query):
        pass

    def mark_as_read(self, document_id):
        pass

    def mark_as_unread(self, document_id):
        pass

    def add_to_favorites(self, document_id):
        pass

    def remove_from_favorites(self, document_id):
        pass

    def add_tag(self, document_id, tag):
        pass

    def remove_tag(self, document_id):
        pass

    def get_document_bibtex(self, document_id):
        pass

    def register_project_routes(self, app):
        app.add_url_rule("/project/get-documents", view_func=self.get_project_documents)
        app.register_blueprint(self.project)
