from database.repository.document_repository import DocumentRepository
from services.notebook_service import NotebookService
from services.project_service import ProjectService
from services.document_service import DocumentService
from bson import ObjectId
from flask import Blueprint, Flask, jsonify, request, json

class ProjectController:
    """
    Controller class responsible for handling all project-related API endpoints,
    including document retrieval, tag and note management, and document renaming.
    """

    def __init__(self, app : Flask):
        """
        Initializes the ProjectController with necessary services and registers routes.

        Args:
            app (Flask): The Flask application instance.
        """
        self.project_service = ProjectService()
        self.document_service = DocumentService()
        self.document_repository = DocumentRepository
        self.notebook_service = NotebookService()
        self.project = Blueprint('project', __name__)
        self.register_project_routes(app)

    def rename_document(self):
        """
        Renames a document based on its ID and the new name provided in the request.

        Returns:
            Response: JSON response indicating success or error status.
        """
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            document_id = ObjectId(data.get('document_id'))
            new_name = data.get('name')
            if not all([user_id, document_id, new_name]):
                return jsonify({'error': 'Missing required fields'}), 400
            result = self.document_service.rename_document(document_id, new_name)
            if result:
                return jsonify({
                    "status": "success",
                    "message": "Document renamed successfully"
                    }), 200
            else:
                return jsonify({
                    "status": "error",
                    "message": "Failed to rename the document"
                }), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_project_documents(self):
        """
        Retrieves documents associated with a project based on various filters and sorting options.

        Returns:
            Response: JSON containing a list of documents or error message.
        """
        try:
            user_id = request.args.get("user_id")
            project_id = request.args.get("project_id")
            raw_sort_states = request.args.get("sort_states")
            sort_states = json.loads(raw_sort_states) if raw_sort_states else []
            filter_state = request.args.get("filter_state")
            tagname = request.args.get("tagname")

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            document_list = []
            documents = []

            if not sort_states:
                if not filter_state:
                    documents = self.document_service.get_project_documents(project_id)
                else:
                    if filter_state == "ByFavourite":
                        documents = self.document_service.filter_documents(project_id, favorite=True)
                    elif filter_state == "IfRead":
                        documents = self.document_service.filter_documents(project_id, read=True)
                    elif filter_state == "ByTag":
                        documents = self.document_service.filter_documents(project_id, tag=tagname)
            else:
                if not filter_state:
                    documents = self.project_service.sort_project_documents(project_id, sort_states[0]["field"], sort_states[0]["order"])
                else:
                    if filter_state == "ByFavourite":
                        documents = self.document_service.get_filtered_and_sorted_documents(project_id, favorite=True, sort_field=sort_states[0]["field"], order=sort_states[0]["order"])
                    elif filter_state == "IfRead":
                        documents = self.document_service.get_filtered_and_sorted_documents(project_id, read=True, sort_field=sort_states[0]["field"], order=sort_states[0]["order"])
                    elif filter_state == "ByTag":
                        documents = self.document_service.get_filtered_and_sorted_documents(project_id, tag=tagname, sort_field=sort_states[0]["field"], order=sort_states[0]["order"])

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
                    "TagName" : document.tag_name,
                    "TagColor" : document.tag_color,
                    "Note" : document.note,
                    "Year": self.document_repository.get_year(str(document.document_id)),
                    "Source": self.document_repository.get_source(str(document.document_id)),
                    "Authors": self.document_service.get_first_author(str(document.document_id)),
                }
                document_list.append(document_object)

            return jsonify({
                "status": "success",
                "documents": document_list,
                "message": "Documents retrieved successfully",
            }), 200

        except Exception as e:
            print(f"Error to get documents from the projects: {str(e)}")
            return jsonify({"error": str(e)}), 500

    def get_project_tags(self):
        """
        Retrieves all tags associated with a project.

        Returns:
            Response: JSON containing tags or an error message.
        """
        try:
            user_id = request.args.get("user_id")
            project_id = request.args.get("project_id")
            if not user_id or not project_id:
                return jsonify({"error": "Missing user_id or project_id"}), 400

            tags_list = self.document_service.get_project_tags(project_id)
            return jsonify({
                "status": "success",
                "tags": tags_list,
                "message": "Tags from projects retrieved successfully",
            }), 200

        except Exception as e:
            print(f"Error in get_project_tags: {e}")
            return jsonify({"error": str(e)}), 500

    def get_project_note(self):
        """
        Retrieves the notebook note associated with a project.

        Returns:
            Response: JSON containing the project note or an error message.
        """
        try:
            user_id = request.args.get("user_id")
            project_id = request.args.get("project_id")
            if not user_id or not project_id:
                return jsonify({"error": "Missing user_id or project_id"}), 400

            note = self.notebook_service.get_projects_notebook(project_id)
            if note is None:
                note = ""
            return jsonify({
                "status": "success",
                "note": note,
                "message": "Notes from projects retrieved successfully",
            }), 200

        except Exception as e:
            print(f"Error in get_project_note: {e}")
            return jsonify({"error": str(e)}), 500

    def save_project_note(self):
        """
        Saves a notebook note for a given project.

        Returns:
            Response: JSON message indicating success or failure.
        """
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            project_id = data.get("project_id")
            note = data.get("note")

            if not user_id or not project_id:
                return jsonify({"error": "Missing user_id or project_id"}), 400

            self.notebook_service.update_project_notebook(project_id, note)
            return jsonify({"message": "Note saved"}), 200
        except Exception as e:
            print(f"Error in save_project_note: {e}")
            return jsonify({"error": str(e)}), 500

    def register_project_routes(self, app):
        """
        Registers all API routes for project operations with the Flask app.

        Args:
            app (Flask): The Flask application instance.
        """
        app.add_url_rule("/project/get-documents", view_func=self.get_project_documents)
        app.add_url_rule("/project/rename", view_func=self.rename_document, methods=['PATCH'])
        app.add_url_rule("/project/note", view_func=self.get_project_note)
        app.add_url_rule("/project/tags", view_func=self.get_project_tags)
        app.add_url_rule("/project/note", view_func=self.save_project_note, methods=['POST'])
        app.register_blueprint(self.project)