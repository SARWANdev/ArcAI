from services.library_service import LibraryService
from services.project_service import ProjectService
from services.document_service import DocumentService

class LibraryController:
    def __init__(self):
        self.library_service = LibraryService()
        self.project_service = ProjectService()
        self.document_service = DocumentService()

    def get_embeddings(self, item_ids=None):
        pass

    def get_project(self, project_id):
        pass

    def search_documents(self, query, filters=None):
        pass

    def create_project(self, user_id, name, description=None, note=None):
        pass

    def download_project(self, project_id):
       pass

    def delete_project(self, project_id):
        pass

    def rename_project(self, project_id, name):
        pass

    def sort_projects(self, sort_by, sort_order):
        pass

    def filter_projects(self, filters):
        pass

    def get_item_metadata(self, item_id, item_type):
        pass
