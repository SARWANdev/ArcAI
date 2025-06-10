from services.project_service import ProjectService
from services.document_service import DocumentService

class ProjectController:
    def __init__(self):
        self.project_service = ProjectService()
        self.document_service = DocumentService()

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

    def get_project_documents(self, project_id):
        pass

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

    def get_document_metadata(self, document_id):
        pass
