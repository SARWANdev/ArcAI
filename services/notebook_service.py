from database.repository.notebook_repository import Notebook as NotebookRepository
from database.repository.document_repository import DocumentRepository
from database.repository.project_repository import Project as ProjectRepository
import io 

class NotebookService:
    """
    Service for managing project and document notebooks, including retrieval,
    updating, and exporting as text files.
    """
    def __init__(self):
        """
        Initialize the NotebookService with required repositories.
        """
        self.notebook_repository = NotebookRepository
        self.document_repository = DocumentRepository
        self.project_repository = ProjectRepository

    def get_projects_notebook(self, project_id):
        """
        Get the notebook content for a given project.

        :param project_id: Project identifier
        :type project_id: str
        :return: Notebook content as a string
        :rtype: str
        """
        note = self.notebook_repository.get_project_notebook(project_id)
        return note

    def get_documents_notebook(self, document_id):
        """
        Get the notebook content for a given document.

        :param document_id: Document identifier
        :type document_id: str
        :return: Notebook content as a string
        :rtype: str
        """
        note = self.notebook_repository.get_document_notebook(document_id)
        return note
    
    def update_document_notebook(self, document_id, note):
        """
        Update the notebook content for a document.

        :param document_id: Document identifier
        :type document_id: str
        :param note: New notebook content
        :type note: str
        :return: True if update was successful, else False
        :rtype: bool
        """
        return NotebookRepository.update_document_notebook(document_id, note)

    def update_project_notebook(self, project_id, note):
        """
        Update the notebook content for a project.

        :param project_id: Project identifier
        :type project_id: str
        :param note: New notebook content
        :type note: str
        :return: True if update was successful, else False
        :rtype: bool
        """
        return NotebookRepository.update_project_notebook(project_id, note)

    def download_documents_notebook(self, document_id):
        """
        Export a document's notebook as a downloadable text file.

        :param document_id: Document identifier
        :type document_id: str
        :return: Tuple of (file buffer, filename)
        :rtype: (io.BytesIO, str)
        """
        notebook = self.get_documents_notebook(document_id)
        document_title = DocumentRepository.get_by_document_id(document_id).get('title')
        notes_title = document_title + 'notes.txt'
        buffer = io.BytesIO()
        buffer.write(notebook.encode('utf-8'))
        return buffer, notes_title

    def download_projects_notebook(self, project_id):
        """
        Export a project's notebook as a downloadable text file.

        :param project_id: Project identifier
        :type project_id: str
        :return: Tuple of (file buffer, filename)
        :rtype: (io.BytesIO, str)
        """
        notebook = self.get_projects_notebook(project_id)
        project_title = ProjectRepository.get_by_project_id(project_id).get('title')
        notes_title = project_title + 'notes.txt'
        buffer = io.BytesIO()
        buffer.write(notebook.encode('utf-8'))
        return buffer, notes_title

