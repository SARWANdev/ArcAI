from database.repository.notebook_repository import Notebook as NotebookRepository
from model.document_reader.notebook import Notebook as NotebookModel
from database.repository.document_repository import Document as DocumentRepository
from database.repository.project_repository import Project as ProjectRepository

class NotebookService:
    def __init__(self):
        self.notebook_repository = NotebookRepository
        self.document_repository = DocumentRepository
        self.project_repository = ProjectRepository

    def create_notebook(self, title, content=None):
        pass

    def get_projects_notebook(self, project_id):
        note = self.notebook_repository.get_project_notebook(project_id)
        return note

    def get_documents_notebook(self, document_id):
        note = self.notebook_repository.get_document_notebook(document_id)
        return note

    def delete_notebook(self, notebook_id):
        pass

    def edit_notebook(self, notebook_id, prompt):
        pass

    def download_notebook(self, notebook_id):
        pass
