from database.repository.notebook_repository import Notebook as NotebookRepository
from model.notebook import Notebook as NotebookModel

class NotebookService:
    def __init__(self):
        self.notebook_repository = NotebookRepository

    def create_notebook(self, title, content=None):
        pass

    def get_notebook(self, notebook_id):
        pass

    def update_notebook(self, notebook_id, title=None, content=None):
        pass

    def delete_notebook(self, notebook_id):
        pass

    def download_notebook(self, notebook_id):
        pass
