from services.project_service import ProjectService
from services.document_service import DocumentService

class ProjectController:
    def __init__(self):
        self.project_service = ProjectService()
        self.document_service = DocumentService()

    def create_project(self, user_id, name, description=None, note=None):
        pass

    def get_project(self, project_id):
        pass

    def get_user_projects(self, user_id):
        pass

    def update_project(self, project_id, name=None, description=None, note=None):
        pass

    def delete_project(self, project_id):
        pass

    def download_project(self, project_id):
        pass

    def get_project_documents(self, project_id):
        pass

    def get_project_embeddings(self, project_id, document_ids=None):
        pass

    def sort_project_documents(self, project_id, sort_by, sort_order):
        pass

    def filter_project_documents(self, project_id, filters):
        pass

    def search_project_documents(self, project_id, query):
        pass
