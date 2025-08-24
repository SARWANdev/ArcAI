from io import BytesIO

from database.repository.document_properties_repository import DocumentPropertiesRepository
from exceptions.document_exceptions import InvalidDocumentNamingException, InvalidServerConnectionException, \
    InvalidProjectIdException, InvalidUserIdException
from services.document_service import DocumentService
from services.download_manager.download_manager import download_file, get_document_bibtex
from services.notebook_service import NotebookService
from database.repository.document_repository import DocumentRepository
from services.ai_service import AIService
from flask import Blueprint,Flask, jsonify, request, send_file, Response
from database.repository.pdf_master_repository import PdfMasterRepository
from bson import ObjectId

from services.upload_manager.server_conection import retrieve_document_content, save_document_content
from exceptions.tag_exceptions import TagException, InvalidTagName, MissingTagColor


class DocumentController:
    """
    Controller class for handling HTTP requests related to document operations.

    Provides methods for uploading, downloading, deleting, and updating documents, 
    as well as handling document metadata like tags, favorites, and notes.
    """
    def __init__(self, app: Flask):
        """
        Initializes the DocumentController with the given Flask app and sets up routes.

        :param app: The Flask app to register the document routes.
        :type app: Flask
        """
        self.document_service = DocumentService()
        self.document = Blueprint('document', __name__)
        self.notebook_service = NotebookService()
        self.document_repository = DocumentRepository
        self.document_properties_repository = DocumentPropertiesRepository
        self.ai_service = AIService()
        self.register_document_routes(app)

    def add_document_tag(self):
        """
        Adds a tag to a document.

        :returns: JSON response with success or error status.
        :rtype: Response
        """
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

        except InvalidTagName as e:
            return jsonify({"error": str(e)}), 400
        except MissingTagColor as e:
            return jsonify({"error": str(e)}), 400
        except TagException as e:
            return jsonify({"error": str(e)}), 409
        except Exception as e:
            print(f"Error in making a tag for the document: {str(e)}")
            return jsonify({"error": str(e)}), 500

    def remove_document_tag(self):
        """
        Removes a tag from a document.

        :returns: JSON response with success or error status.
        :rtype: Response
        """
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
            return jsonify({"error": str(e)}), 500

    def upload_document(self):
        """
        Uploads a document to the server.

        :returns: JSON response with success or error status.
        :rtype: Response
        """
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

        except InvalidDocumentNamingException as e:
            return jsonify({"error": str(e)}), 400
        except InvalidUserIdException as e:
            return jsonify({"error": str(e)}), 409
        except InvalidProjectIdException as e:
            return jsonify({"error": str(e)}), 409
        except InvalidServerConnectionException as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            print(f"Error to get upload the document: {str(e)}")
            return jsonify({"error": str(e)}), 500

    def get_document(self):
        """
        Uploads a document to the server.

        :returns: JSON response with success or error status.
        :rtype: Response
        """
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
            return jsonify({"error": str(e)}), 500

    def delete_document(self):
        """
        Deletes a document from the server.

        :returns: JSON response with success or error status.
        :rtype: Response
        """
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
            return jsonify({"error": str(e)}), 500

    def save_document(self):
        """
        Deletes a document from the server.

        :returns: JSON response with success or error status.
        :rtype: Response
        """
        try:
            uploaded_file = request.files['file']
            file_bytes = uploaded_file.read()
            document_id = request.form['document_id']
            file_path = self.document_repository.get_path(document_id)
            save_document_content(file_path, file_bytes)
            return jsonify({"status": "success", "message": "File saved"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def make_document_favourite(self):
        """
        Marks a document as favorite.

        :returns: JSON response with success or error status.
        :rtype: Response
        """
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
            return jsonify({"error": str(e)}), 500

    def delete_favourite(self):
        """
        Removes a document from the favorites.

        :returns: JSON response with success or error status.
        :rtype: Response
        """
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
            return jsonify({"error": str(e)}), 500

    def mark_document_read(self):
        """
        Marks a document as read.

        :returns: JSON response with success or error status.
        :rtype: Response
        """
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
            return jsonify({"error": str(e)}), 500

    def delete_document_read(self):
        """
        Marks a document as unread.

        :returns: JSON response with success or error status.
        :rtype: Response
        """
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
            return jsonify({"error": str(e)}), 500

    def get_document_note(self):
        """
        Retrieves the note for a document.

        :returns: JSON response with the note content.
        :rtype: Response
        """
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
            return jsonify({"error": str(e)}), 500

    def save_document_note(self):
        """
        Saves the note for a document.

        :returns: JSON response with success or error status.
        :rtype: Response
        """
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
            return jsonify({"error": str(e)}), 500

    def duplicate_document(self):
        """
        Duplicates a document to a new project.

        :returns: JSON response with success or error status.
        :rtype: Response
        """
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
            return jsonify({"error": str(e)}), 500

    def download_document(self):
        """
        Downloads a document as a ZIP file.

        :returns: JSON response with the ZIP file or error status.
        :rtype: Response
        """
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
            return jsonify({"error": str(e)}), 500

    def move_document(self):
        """
        Moves a document to another project.

        :returns: JSON response to confirm a documents move
        """
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

            return jsonify({"message": "Document moved successfully"}), 200

        except Exception as e:
            print(f"Error in move_document: {e}")
            return jsonify({"error": str(e)}), 500

    def get_document_bibtex(self):
        """
        Gets a documents BibTex.

        :returns: Response with documents BibTex.
        :rtype: Response
        """
        try:
            user_id = request.args.get("user_id")
            document_id = request.args.get("document_id")

            if not user_id or not document_id:
                return jsonify({"error": "Missing user_id or document_id"}), 400

            bibtex = get_document_bibtex(document_id)  # This should return a string

            if not bibtex:
                return jsonify({"error": "BibTeX not found"}), 404

            # Return as a file response
            return Response(
                bibtex,
                mimetype="application/x-bibtex",
                headers={"Content-Disposition": "attachment;filename=export.bib"}
            )

        except Exception as e:
            print(f"Error in get_document_bibtex: {e}")
            return jsonify({"error": str(e)}), 500

    def set_document_bibtex(self):
        """
        Sets a documets BibTex.

        :response: JSON message with actions response. 
        """
        try:
            data = request.json  # get JSON body
            user_id = data.get("userid")
            document_id = data.get("document_id")
            bibtex = data.get("bibtex")

            if not user_id or not document_id:
                return jsonify({"error": "Missing user_id or document_id"}), 400

            pdf_master_id = self.document_repository.get_pdf_master_id(document_id)
            PdfMasterRepository.set_bibtex(pdf_master_id, bibtex)

            if not bibtex:
                return jsonify({"error": "BibTeX not found"}), 404

            # TODO: Actually save the bibtex to the database or file
            return jsonify({"message": "Bibtex saved successfully"}), 200

        except Exception as e:
            print(f"Error in set_document_bibtex: {e}")
            return jsonify({"error": str(e)}), 500

    def get_document_bibtex_string(self):
        """
        Gets a documents BibTex as str.

        :response: JSON message with actions response.
        """
        try:
            user_id = request.args.get("userid")  # Get from query string
            document_id = request.args.get("document_id")

            if not user_id or not document_id:
                return jsonify({"error": "Missing user_id or document_id"}), 400

            pdf_master_id = self.document_repository.get_pdf_master_id(document_id)
            bibtex_string = PdfMasterRepository.get_bibtex(pdf_master_id)


            return jsonify({"message": "Bibtex retrieved successfully",
                            "data": {"BibTeX": bibtex_string}
                            }), 200

        except Exception as e:
            print(f"Error in get_document_bibtex_string: {e}")
            return jsonify({"error": str(e)}), 500

    def get_project_from_document(self):
        try:
            user_id = request.args.get("user_id")  # fixed naming
            document_id = request.args.get("document_id")
            print(user_id, document_id)
            if not user_id or not document_id:
                return jsonify({"error": "Missing user_id or document_id"}), 400

            project = self.document_properties_repository.get_project_id_and_name(document_id)
            # Assume this returns {"projectId": "...", "projectName": "..."}
            print(project)
            return jsonify(project), 200

        except Exception as e:
            print(f"Error in get_project_from_document: {e}")
            return jsonify({"error": str(e)}), 500

    def register_document_routes(self, app):
        """
        Registers all project-related API routes to the given Flask app.

        :param app: Flask application instance.
        """
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
        app.add_url_rule("/document/bibtex", view_func=self.get_document_bibtex)
        app.add_url_rule("/document/bibtex/set", view_func=self.set_document_bibtex, methods=["POST"])
        app.add_url_rule("/document/project", view_func=self.get_project_from_document)
        app.add_url_rule("/document/bibtex/string", view_func=self.get_document_bibtex_string)
        app.register_blueprint(self.document)