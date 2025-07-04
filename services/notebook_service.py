from database.repository.notebook_repository import Notebook as NotebookRepository
from model.document_reader.notebook import Notebook as NotebookModel
from database.repository.document_repository import Document as DocumentRepository
from database.repository.project_repository import Project as ProjectRepository
import io 

class NotebookService:
    def __init__(self):
        self.notebook_repository = NotebookRepository
        self.document_repository = DocumentRepository
        self.project_repository = ProjectRepository

    def create_notebook(self, title, content=None): #TODO: fit either model or repository to create notebooks
        pass

    def get_projects_notebook(self, project_id):
        note = self.notebook_repository.get_project_notebook(project_id)
        return note

    def get_documents_notebook(self, document_id):
        note = self.notebook_repository.get_document_notebook(document_id)
        return note
    
    # Clears a notebook by updating it with an empty string
    def clear_document_notebook(self, document_id):
        return NotebookRepository.update_document_notebook(document_id, '')
    
    def clear_project_notebook(self, project_id):
        return NotebookRepository.update_project_notebook(project_id, '')

    # Updates a notebook
    def update_document_notebook(self, document_id, note):
        return NotebookRepository.update_document_notebook(document_id, note)

    def update_project_notebook(self, project_id, note):
        return NotebookRepository.update_project_notebook(project_id, note)

    # Gets a notebook and returns it as a txt file to be downloaded
    def download_documents_notebook(self, document_id):
        notebook = self.get_documents_notebook(document_id)
        document_title = DocumentRepository.get_by_document_id(document_id).get('title')
        notes_title = document_title + 'notes.txt'
        buffer = io.BytesIO()
        buffer.write(notebook.encode('utf-8'))
        return buffer, notes_title

    def download_projects_notebook(self, project_id):
        notebook = self.get_projects_notebook(project_id)
        project_title = ProjectRepository.get_by_project_id(project_id).get('title')
        notes_title = project_title + 'notes.txt'
        buffer = io.BytesIO()
        buffer.write(notebook.encode('utf-8'))
        return buffer, notes_title

