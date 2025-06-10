from database.repository.document_repository import Document as DocumentRepository
from model.document_reader.document import Document as DocumentModel

class DocumentService:
   
    def __init__(self):
        self.document_repository = DocumentRepository

    def create_document(self, project_id, name, path, note=None):
        pass

    def get_document(self, document_id):
        pass

    def get_project_documents(self, project_id):
        pass

    def update_document(self, document_id, name=None, note=None):
        pass

    def delete_document(self, document_id):
        pass

    def mark_as_read(self, document_id):
        pass

    def mark_as_unread(self, document_id):
        pass

    def download_document(self, document_id):
        pass

    def add_to_favorites(self, document_id):
        pass

    def remove_from_favorites(self, document_id):
        pass

    def add_tag(self, document_id, tag):
        pass

    def remove_tag(self, document_id):
        pass

    def get_document_tags(self, document_id):
        pass

    def highlight_document(self, document_id, text):
        pass

    def process_document_metadata(self, document_id):
        pass

    def duplicate_document(self, project_id, document_id):
        pass

    def extract_text_from_document(self, document_id):
        pass

    def get_text_chunks_from_document(self, document_id):
        pass

    def download_bibtex(self, document_id):
        pass
    