from services.notebook_service import NotebookService

class NotebookController:
    def __init__(self):
        self.notebook_service = NotebookService()

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
