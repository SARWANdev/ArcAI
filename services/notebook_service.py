from database.repository.notebook_repository import Notebook as NotebookRepository
from model.document_reader.notebook import Notebook as NotebookModel

class NotebookService:
    def __init__(self):
        self.notebook_repository = NotebookRepository

    def create_notebook(self, title, content=None):
        pass

    def get_notebook(self, notebook_id):
        pass

    def delete_notebook(self, notebook_id):
        pass

    def edit_notebook(self, notebook_id, prompt):
        pass

    def download_notebook(self, notebook_id):
        pass
