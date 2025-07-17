from database.repository.document_repository import DocumentDataBase as DocumentRepository
from services.project_service import ProjectService
from services.document_service import DocumentService
from flask import Blueprint, Flask, jsonify, request, json

class ProjectController:
    def __init__(self, app : Flask):
        self.project_service = ProjectService()
        self.document_service = DocumentService()
        self.document_repository = DocumentRepository
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
            project_id = request.args.get("project_id")
            raw_sort_states = request.args.get("sort_states")
            sort_states = json.loads(raw_sort_states) if raw_sort_states else []
            filter_state = request.args.get("filter_state")

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            sort_criteria = []
            document_list = []

            if not sort_states:
                documents = self.document_service.get_project_documents(project_id)
            else:
                for sort_state in sort_states:
                    sort_tuple = (sort_state["field"].lower(), sort_state["order"])
                    sort_criteria.append(sort_tuple)
                documents = self.project_service.sort_project_documents(project_id, sort_criteria)

            # Check if documents is None
            if documents is None:
                documents = []

            for document in documents:
                document_object = {
                    "DocumentId": str(document.document_id),
                    "ProjectId": str(document.project_id),
                    "Title": document.name,
                    "Read": document.read,
                    "CreatedAt": document.created_at,
                    "Favorite": document.favorite,
                    "Year": self.document_repository.get_year(str(document.document_id)),
                    "Source": self.document_repository.get_source(str(document.document_id)),
                    "Authors": self.document_repository.get_authors(str(document.document_id)),
                }
                document_list.append(document_object)

            return jsonify({
                "status": "success",
                "documents": document_list,
                "message": "Documents retrieved successfully",
            }), 200

        except Exception as e:
            print(f"Error to get documents from the projects: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to retrieve documents",
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
