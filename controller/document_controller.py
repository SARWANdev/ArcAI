from io import BytesIO
from services.document_service import DocumentService
from services.notebook_service import NotebookService
from database.repository.document_repository import DocumentDataBase
from services.ai_service import AIService
from flask import Blueprint,Flask, jsonify, request, send_file

from services.upload_manager.server_conection import retrieve_document_content, save_document_content


class DocumentController:
    def __init__(self, app: Flask):
        self.document_service = DocumentService()
        self.document = Blueprint('document', __name__)
        self.notebook_service = NotebookService()
        self.document_repository = DocumentDataBase
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

            self.document_service.upload_file(file, user_sub, project_id)

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

    def get_document(self):
        try:
            document_id = request.args.get("document_id")

            file_path = self.document_repository.get_path(document_id)
            file_bytes = retrieve_document_content(file_path)

            if not file_bytes:
                raise ValueError("File content is empty or None")

            return send_file(
                BytesIO(file_bytes),
                mimetype="application/pdf",
                as_attachment=False,
                download_name=f"{document_id}.pdf"
            )

        except Exception as e:
            print(f"Error sending file: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to send the document file",
                "error": str(e)
            }), 500

    def delete_document(self):
        try:
            # Get parameters from query string
            data = request.get_json()
            user_id = data.get("user_id")
            document_id = data.get("document_id")

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            self.document_service.delete_document(document_id)
            # Return both success message
            return jsonify({
                "status": "success",
                "message": "Projects deleted successfully",
            }), 200

        except Exception as e:
            print(f"Error in deleting the document: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to delete the document",
                "error": str(e)
            }), 500

    def save_document(self):
        try:
            uploaded_file = request.files['file']
            file_bytes = uploaded_file.read()
            document_id = request.form['document_id']
            file_path = self.document_repository.get_path(document_id)
            save_document_content(file_path, file_bytes)
            return jsonify({"status": "success", "message": "File saved"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500


    def register_document_routes(self, app):
        app.add_url_rule("/document/upload", view_func=self.upload_document, methods=["POST"])
        app.add_url_rule("/document/delete", view_func=self.delete_document, methods=["DELETE"])
        app.add_url_rule("/document/get-document", view_func=self.get_document)
        app.add_url_rule("/document/save", view_func=self.save_document, methods=["POST"])
        app.register_blueprint(self.document)