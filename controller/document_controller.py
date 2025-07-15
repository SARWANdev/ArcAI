import os

from services.document_service import DocumentService
from services.notebook_service import NotebookService
from services.ai_service import AIService
from werkzeug.utils import secure_filename
from flask import Blueprint,Flask, jsonify, request


class DocumentController:
    def __init__(self, app: Flask):
        self.document_service = DocumentService()
        self.document = Blueprint('document', __name__)
        self.notebook_service = NotebookService()
        self.ai_service = AIService()
        self.register_document_routes(app)

    def download_document(self, document_id):
        pass

    def download_notebook(self, notebook_id):
        pass

    def edit_notebook(self, notebook_id, prompt):
        pass

    def highlight_document(self, document_id, text):
        pass

    def get_document_metadata(self, document_id):
        pass

    def get_document_summary(self, document_id):
        pass

    def get_chat(self, chat_id):
        pass

    def follow_up(self, chat_id, prompt):
        pass

    def upload_document(self):
        try:
            # Validate file part
            if "file" not in request.files:
                return jsonify({"error": "No file part in the request"}), 400

            file = request.files["file"]
            user_sub = request.form.get("user_sub")
            project_id = request.form.get("project_id")

            if not file or file.filename.strip() == "":
                return jsonify({"error": "No selected file"}), 400

            print(f"The user : {user_sub} wants in the project : {project_id} the file {file.filename} has been uploaded")

            self.document_service.upload_file(file, file.filename, user_sub, project_id)

            return jsonify({
                "status": "success",
                "message": "The document has been uploaded successfully",
            }), 200

        except Exception as e:
            print(f"Error to get upload the document: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to upload the document in the server",
                "error": str(e)
            }), 500



    def get_document_path(self):
        try:
            # Get parameters from query string
            user_id = request.args.get("user_id")
            document_id = request.args.get("document_id")


            print(f"The user {user_id} and want the path of the document id {document_id}")
            return jsonify({
                "status": "success",
                "message": "Documents path retrieved successfully",
            }), 200

        except Exception as e:
            print(f"Error to get path of the document: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to retrieve the path of the document",
                "error": str(e)
            }), 500


    def register_document_routes(self, app):
        app.add_url_rule("/document/upload", view_func=self.upload_document, methods=["POST"])
        app.add_url_rule("/document/getpath", view_func=self.get_document_path)
        app.register_blueprint(self.document)