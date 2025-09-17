from io import BytesIO

from services.download_manager.download_manager import download_project
from services.library_service import LibraryService
from services.project_service import ProjectService
from services.document_manager.document_service import DocumentService
from flask import Blueprint, Flask, jsonify, request, send_file
from exceptions.base_exceptions import NotFoundException, InvalidNameException, DuplicateNameException


class LibraryController:
    """
    Controller for managing user libraries, including creating, retrieving,
    deleting, renaming projects and searching or downloading documents.
    """

    def __init__(self, app: Flask):
        """
        Initializes the LibraryController with service instances and registers routes.

        :param app: Flask app instance to which the routes will be registered.
        """
        self.library_service = LibraryService()
        self.project_service = ProjectService()
        self.document_service = DocumentService()
        self.library = Blueprint('library', __name__)
        self.register_library_routes(app)

    def create_project(self):
        """
        Creates a new project for the user based on provided JSON data.

        Expected JSON body:
        - user_id: ID of the user
        - name: Name of the new project

        :return: JSON response indicating success or failure.
        """
        try:
            data = request.get_json()

            user_id = data.get("user_id")
            name = data.get("name")

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            if not name:
                return jsonify({"error": "Project name is required"}), 400

            project = self.project_service.create_project(user_id, name)

            return jsonify({
                "success": "Project created successfully",
                "project": {
                    "id": project.id,
                    "name": project.project_name,
                    "user_id": project.user_id
                }
            }), 201

        except InvalidNameException as e:
            return jsonify({"error": str(e)}), 400
        except DuplicateNameException as e:
            return jsonify({"error": str(e)}), 409
        except Exception as e:
            return jsonify({"error": f"Failed to create project: {str(e)}"}), 500

    def get_user_projects(self):
        """
        Retrieves a list of projects for a given user, optionally sorted.

        Query parameters:
        - user_id: ID of the user (required)
        - sort_by: Field to sort by ('Title', 'CreatedAt', or 'LastUpdated')
        - order: Sorting order ('asc' or 'desc')

        :return: JSON response containing the list of projects or error.
        """
        try:
            user_id = request.args.get("user_id")
            sort_by = request.args.get("sort_by", "LastUpdated")
            order = request.args.get("order", "desc")

            if sort_by == "Title":
                sort_by = "name"
            elif sort_by == "CreatedAt":
                sort_by = "created"
            elif sort_by == "LastUpdated":
                sort_by = "updated"

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            project_model_list = self.library_service.sort_library(user_id, sort_by, order)

            project_list = [
                {
                    "Title": model.project_name,
                    "CreatedAt": model.created_at,
                    "LastUpdated": model.updated_at,
                    "ProjectId": str(model.id)
                }
                for model in project_model_list
            ]

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
            return jsonify({"error": str(e)}), 500

    def download_project(self):
        """
        Downloads a project as a ZIP file.

        Query parameters:
        - user_id: ID of the user
        - project_id: ID of the project to download

        :return: ZIP file response if successful, else error response.
        """
        try:
            user_id = request.args.get("user_id")
            project_id = request.args.get("project_id")
            if not user_id or not project_id:
                return jsonify({"error": "Missing user_id or project_id"}), 400

            project = download_project(project_id)

            if not project:
                return jsonify({"error": "Project could not be downloaded"}), 404

            zip_stream = BytesIO(project)

            return send_file(
                zip_stream,
                mimetype="application/zip",
                download_name=f"project_{project_id}.zip",
                as_attachment=True
            )

        except Exception as e:
            print(f"Error in download_project: {e}")
            return jsonify({"error": str(e)}), 500

    def delete_project(self):
        """
        Deletes a project specified by project ID.

        Expected JSON body:
        - user_id: ID of the user
        - project_id: ID of the project to delete

        :return: JSON response indicating success or failure.
        """
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            project_id = data.get("project_id")

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            self.project_service.delete_project(project_id)

            return jsonify({
                "status": "success",
                "message": "Projects deleted successfully",
            }), 200

        except Exception as e:
            print(f"Error in delete_project: {str(e)}")
            return jsonify({"error": str(e)}), 500

    def rename_project(self):
        """
        Renames a project to a new name.

        Expected JSON body:
        - user_id: ID of the user
        - project_id: ID of the project to rename
        - name: New name for the project

        :return: JSON response indicating success or failure.
        """
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            project_id = data.get('project_id')
            new_name = data.get('name')

            if not all([user_id, project_id, new_name]):
                return jsonify({'error': 'Missing required fields: user_id, project_id, or name'}), 400

            if not new_name.strip():
                return jsonify({'error': 'Project name cannot be empty'}), 400

            result = self.project_service.rename_project(project_id, new_name)
            
            if result:
                return jsonify({
                    "status": "success",
                    "message": "Project renamed successfully"
                }), 200
            else:
                return jsonify({
                    "status": "error",
                    "message": "Failed to rename the project"
                }), 500

        except InvalidNameException as e:
            return jsonify({"error": str(e)}), 400
        except DuplicateNameException as e:
            return jsonify({"error": str(e)}), 409
        except NotFoundException as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": f"Failed to rename project: {str(e)}"}), 500

    def search_documents(self):
        """
        Searches for documents matching the given query for a user.

        Query parameters:
        - user_id: ID of the user
        - query: Search string to look for in documents

        :return: JSON response with search results or error.
        """
        try:
            user_id = request.args.get("user_id")
            query = request.args.get("query")

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            searches = self.document_service.search_documents(user_id, query)
            documents = []
            for document in searches:
                dictionary = {"Title": document.name, "DocumentId": document.document_id}
                documents.append(dictionary)

            return jsonify({
                "status": "success",
                "results": documents,
                "message": "Search retrieved successfully",
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def register_library_routes(self, app):
        """
        Registers all library-related API routes to the given Flask app.

        :param app: Flask application instance.
        """
        self.library.add_url_rule("/library/create-project", view_func=self.create_project, methods=["POST"])
        self.library.add_url_rule("/library/download", view_func=self.download_project)
        self.library.add_url_rule("/library/get-projects", view_func=self.get_user_projects)
        self.library.add_url_rule("/library/delete-project", view_func=self.delete_project, methods=["DELETE"])
        self.library.add_url_rule("/library/rename-project", view_func=self.rename_project, methods=["PATCH"])
        self.library.add_url_rule("/library/search/document", view_func=self.search_documents)
        app.register_blueprint(self.library)