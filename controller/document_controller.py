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
        home_dir = os.path.expanduser("~")
        document_dir = os.path.join(home_dir, 'Documents')
        upload_folder = os.path.join(document_dir, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        safe_filename = secure_filename(file.filename)
        save_path = os.path.join(upload_folder, safe_filename)
        file.save(save_path)

        return jsonify({
            "message": "File uploaded successfully",
            "saved_path": save_path
        }), 200

    def register_document_routes(self, app):
        app.add_url_rule("/document/upload", view_func=self.upload_document, methods=["POST"])
        app.register_blueprint(self.document)