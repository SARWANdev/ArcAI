from io import BytesIO
from services.document_service import DocumentService
from services.download_manager.download_manager import download_file
from services.notebook_service import NotebookService
from database.repository.document_repository import DocumentDataBase
from services.ai_service import AIService
from flask import Blueprint,Flask, jsonify, request, send_file
from bson import ObjectId

from services.upload_manager.server_conection import retrieve_document_content, save_document_content


class DocumentController:
    def __init__(self, app: Flask):
        self.document_service = DocumentService()
        self.document = Blueprint('document', __name__)
        self.notebook_service = NotebookService()
        self.document_repository = DocumentDataBase
        self.ai_service = AIService()
        self.register_document_routes(app)

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

    def add_document_tag(self):
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            tag_name = data.get("tag_name")
            selected_colour = data.get("selected_colour")
            document_id = ObjectId(data.get("document_id"))

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            self.document_service.add_tag(document_id, tag_name, selected_colour)

            return jsonify({
                "status": "success",
                "message": "The tag has been added to the document successfully",
            }), 200

        except Exception as e:
            print(f"Error in making a tag for the document: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to make tag for the document",
                "error": str(e)
            }), 500

    def remove_document_tag(self):
        try:
            # Get parameters from query string
            data = request.get_json()
            user_id = data.get("user_id")
            document_id = data.get("document_id")

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            self.document_service.remove_tag(ObjectId(document_id))
            # Return both success message
            return jsonify({
                "status": "success",
                "message": "Tag deleted successfully",
            }), 200

        except Exception as e:
            print(f"Error in deleting the tag for the document: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to delete the tag for the document",
                "error": str(e)
            }), 500

    def upload_document(self):
        try:
            # Validate file part
            if "file" not in request.files:
                return jsonify({"error": "No file part in the request"}), 400

            file = request.files["file"]
            user_sub = request.form.get("user_sub")
            project_id = request.form.get("project_id")
            print(user_sub)
            print(project_id)

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

    def make_document_favourite(self):
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            document_id = ObjectId(data.get("document_id"))
            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            self.document_service.add_to_favorites(document_id)

            return jsonify({
                "status": "success",
                "message": "The document has been favourite successfully",
            }), 200

        except Exception as e:
            print(f"Error in favouring the document: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to favourite the document",
                "error": str(e)
            }), 500


    def delete_favourite(self):
        try:
            # Get parameters from query string
            data = request.get_json()
            user_id = data.get("user_id")
            document_id = ObjectId(data.get("document_id"))

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            self.document_service.remove_from_favorites(document_id)
            # Return both success message
            return jsonify({
                "status": "success",
                "message": "Projects unfavoured successfully",
            }), 200

        except Exception as e:
            print(f"Error in unfavouring the document: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to un-favour the document",
                "error": str(e)
            }), 500

    def mark_document_read(self):
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            document_id = ObjectId(data.get("document_id"))

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            self.document_service.mark_as_read(document_id)

            return jsonify({
                "status": "success",
                "message": "The document has been marked as read successfully",
            }), 200

        except Exception as e:
            print(f"Error in marking the document as read: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to mark document as read",
                "error": str(e)
            }), 500

    def delete_document_read(self):
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            document_id = ObjectId(data.get("document_id"))

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            self.document_service.mark_as_unread(document_id)

            return jsonify({
                "status": "success",
                "message": "The document has been unmarked as read successfully",
            }), 200

        except Exception as e:
            print(f"Error in unmarking the document as read: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to unmark document as read",
                "error":str(e)
            }), 500

    def get_document_note(self):
        try:
            user_id = request.args.get("user_id")
            document_id = request.args.get("document_id")
            if not user_id or not document_id:
                return jsonify({"error": "Missing user_id or project_id"}), 400

            note = self.notebook_service.get_documents_notebook(document_id)
            if note is None:
                note = ""
            return jsonify({
                "status": "success",
                "note": note,
                "message": "Notes from document retrieved successfully",
            }), 200

        except Exception as e:
            # Log the error for debugging
            print(f"Error in get_document_note: {e}")
            return jsonify({"error": "Internal server error"}), 500

    def save_document_note(self):
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            document_id = data.get("document_id")
            note = data.get("note")
            if not user_id or not document_id:
                return jsonify({"error": "Missing user_id or project_id"}), 400

            self.notebook_service.update_document_notebook(document_id, note)
            return jsonify({"message": "Note saved"}), 200
        except Exception as e:
            print(f"Error in save_document_note: {e}")
            return jsonify({"error": "Internal server error"}), 500


    def duplicate_document(self):
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            project_id = data.get("project_id")
            document_id = data.get("document_id")
            if not user_id or not project_id or not document_id:
                return jsonify({"error": "Missing user_id or project_id or document_id"}), 400

            self.document_service.duplicate_document(document_id, project_id)
            return jsonify({"message": "Document duplicated"}), 200
        except Exception as e:
            print(f"Error in duplicate_document: {e}")
            return jsonify({"error": "Internal server error"}), 500


    def get_document_bibtex(self):
        try:
            user_id = request.args.get("user_id")
            document_id = request.args.get("document_id")
            print(user_id, document_id)
            if not user_id or not document_id:
                return jsonify({"error": "Missing user_id or project_id"}), 400


            return jsonify({
                "status": "success",
                "message": "Bibtex from document retrieved successfully",
            }), 200

        except Exception as e:
            print(f"Error in get_document_bibtex: {e}")
            return jsonify({"error": "Internal server error"}), 500

    def download_document(self):
        try:
            # Extract query parameters
            user_id = request.args.get("user_id")
            document_id = request.args.get("document_id")

            if not user_id or not document_id:
                return jsonify({"error": "Missing user_id or document_id"}), 400

            # Retrieve ZIP file bytes from your helper function
            file_bytes = download_file(document_id)  # Should return raw zip bytes

            if not file_bytes:
                return jsonify({"error": "Document could not be downloaded"}), 404

            # Create an in-memory file object from the bytes
            zip_stream = BytesIO(file_bytes)

            # Return the file as a download
            return send_file(
                zip_stream,
                mimetype="application/zip",
                download_name=f"document_{document_id}.zip",  # Filename when downloading
                as_attachment=True  # Forces download
            )

        except Exception as e:
            print(f"Error in download_document: {e}")
            return jsonify({"error": "Internal server error"}), 500

    def move_document(self):
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            document_id = data.get("document_id")
            project_id = data.get("project_id")

            # Validate input
            if not user_id or not document_id or not project_id:
                return jsonify({"error": "Missing user_id, document_id, or project_id"}), 400

            self.document_service.move_document(document_id, project_id)

            # --- Database logic to move the document ---
            # For example:
            print(user_id, document_id, project_id)

            return jsonify({"message": "Document moved successfully"}), 200

        except Exception as e:
            print(f"Error in move_document: {e}")
            return jsonify({"error": "Internal server error"}), 500


    def register_document_routes(self, app):
        app.add_url_rule("/document/upload", view_func=self.upload_document, methods=["POST"])
        app.add_url_rule("/document/delete", view_func=self.delete_document, methods=["DELETE"])
        app.add_url_rule("/document/get-document", view_func=self.get_document)
        app.add_url_rule("/document/duplicate", view_func=self.duplicate_document, methods=["POST"])
        app.add_url_rule("/document/save", view_func=self.save_document, methods=["POST"])
        app.add_url_rule("/document/favourite", view_func=self.make_document_favourite, methods=["POST"])
        app.add_url_rule("/document/favourite", view_func=self.delete_favourite, methods=["DELETE"])
        app.add_url_rule("/document/read", view_func=self.mark_document_read, methods=["POST"])
        app.add_url_rule("/document/read", view_func=self.delete_document_read, methods=["DELETE"])
        app.add_url_rule("/document/tag", view_func=self.add_document_tag, methods=["POST"])
        app.add_url_rule("/document/tag", view_func=self.remove_document_tag, methods=["DELETE"])
        app.add_url_rule("/document/note", view_func=self.get_document_note)
        app.add_url_rule("/document/note", view_func=self.save_document_note, methods=['POST'])
        app.add_url_rule("/document/move", view_func=self.move_document, methods=["POST"])
        app.add_url_rule("/document/download", view_func=self.download_document)
        app.register_blueprint(self.document)