from database.repository.notebook_repository import Notebook as NotebookRepository
from database.repository.document_repository import DocumentRepository
from database.repository.project_repository import Project as ProjectRepository
from exceptions.notebook_exceptions import InvalidNoteContent, NotebookSaveException, NotebookNotFoundError
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

    def _validate_note_content(self, note: str):
        """
        Validate note content before saving.
        
        :param note: The note content to validate
        :type note: str
        :raises InvalidNoteContent: If the note content is invalid
        """
        if note is None:
            note = ""
        
        # Only check if note is too long - that's the only restriction that makes sense
        if len(note) > InvalidNoteContent.MAX_NOTE_LENGTH:
            raise InvalidNoteContent(
                f"Note content cannot exceed {InvalidNoteContent.MAX_NOTE_LENGTH} characters. "
                f"Current length: {len(note)} characters"
            )
        
        # No character restrictions - let users write whatever they want

    def get_projects_notebook(self, project_id):
        """
        Get the notebook content for a given project.

        :param project_id: Project identifier
        :type project_id: str
        :return: Notebook content as a string
        :rtype: str
        :raises NotebookNotFoundError: If the project notebook is not found
        """
        try:
            note = self.notebook_repository.get_project_notebook(project_id)
            if note is None:
                raise NotebookNotFoundError("project", project_id)
            return note
        except Exception as e:
            if isinstance(e, NotebookNotFoundError):
                raise
            raise NotebookSaveException(f"Failed to retrieve project notebook: {str(e)}")

    def get_documents_notebook(self, document_id):
        """
        Get the notebook content for a given document.

        :param document_id: Document identifier
        :type document_id: str
        :return: Notebook content as a string
        :rtype: str
        :raises NotebookNotFoundError: If the document notebook is not found
        """
        try:
            note = self.notebook_repository.get_document_notebook(document_id)
            if note is None:
                raise NotebookNotFoundError("document", document_id)
            return note
        except Exception as e:
            if isinstance(e, NotebookNotFoundError):
                raise
            raise NotebookSaveException(f"Failed to retrieve document notebook: {str(e)}")
    
    def update_document_notebook(self, document_id, note):
        """
        Update the notebook content for a document.

        :param document_id: Document identifier
        :type document_id: str
        :param note: New notebook content
        :type note: str
        :return: True if update was successful, else False
        :rtype: bool
        :raises InvalidNoteContent: If the note content is invalid
        :raises NotebookSaveException: If the save operation fails
        """
        try:
            # Validate note content before saving
            self._validate_note_content(note)
            
            # Attempt to save
            result = NotebookRepository.update_document_notebook(document_id, note)
            
            if not result:
                raise NotebookSaveException("Database update returned False")
                
            return result
            
        except InvalidNoteContent:
            raise  # Re-raise validation errors
        except Exception as e:
            raise NotebookSaveException(f"Failed to save document notebook: {str(e)}")

    def update_project_notebook(self, project_id, note):
        """
        Update the notebook content for a project.

        :param project_id: Project identifier
        :type project_id: str
        :param note: New notebook content
        :type note: str
        :return: True if update was successful, else False
        :rtype: bool
        :raises InvalidNoteContent: If the note content is invalid
        :raises NotebookSaveException: If the save operation fails
        """
        try:
            # Validate note content before saving
            self._validate_note_content(note)
            
            # Attempt to save
            result = NotebookRepository.update_project_notebook(project_id, note)
            
            if not result:
                raise NotebookSaveException("Database update returned False")
                
            return result
            
        except InvalidNoteContent:
            raise  # Re-raise validation errors
        except Exception as e:
            raise NotebookSaveException(f"Failed to save project notebook: {str(e)}")

    def download_documents_notebook(self, document_id):
        """
        Export a document's notebook as a downloadable text file.

        :param document_id: Document identifier
        :type document_id: str
        :return: Tuple of (file buffer, filename)
        :rtype: (io.BytesIO, str)
        """
        notebook = self.get_documents_notebook(document_id)
        document_title = DocumentRepository.get_by_document_id(document_id).get('title') or ""
        notes_title = f"{document_title}notes.txt"
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
        project_title = ProjectRepository.get_project_by_id(project_id).get('title') or ""
        notes_title = f"{project_title}notes.txt"
        buffer = io.BytesIO()
        buffer.write(notebook.encode('utf-8'))
        return buffer, notes_title