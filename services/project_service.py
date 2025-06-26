from database.repository.project_repository import Project as ProjectRepository
from model.document_reader.project import Project as ProjectModel

class ProjectService:
    def __init__(self):
        self.project_repository = ProjectRepository

    def create_project(self, user_id, name, description=None, note=None):
        pass

    def get_project(self, project_id):
        pass

    def get_user_projects(self, user_id):
        pass

    def delete_project(self, project_id):
        pass

    def rename_project(self, project_id, name):
        self.project_repository.update_name(project_id, name)

    def download_project(self, project_id):
        pass

    def get_project_embeddings(self, project_id, document_ids=None):
        pass

    def process_project_metadata(self, project_id):
        pass

    def generate_project_summary(self, project_id):
        pass
