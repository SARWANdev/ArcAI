import pytest
from unittest.mock import patch
from services.notebook_service import NotebookService
import io
from exceptions.notebook_exceptions import InvalidNoteContent

@pytest.fixture
def notebook_service():
    return NotebookService()

def test_get_projects_notebook(notebook_service):
    with patch.object(notebook_service.notebook_repository, 'get_project_notebook', return_value='project notes'):
        notes = notebook_service.get_projects_notebook('proj1')
        assert notes == 'project notes'

def test_get_documents_notebook(notebook_service):
    with patch.object(notebook_service.notebook_repository, 'get_document_notebook', return_value='doc notes'):
        notes = notebook_service.get_documents_notebook('doc1')
        assert notes == 'doc notes'

def test_update_document_notebook(notebook_service):
    with patch('services.notebook_service.NotebookRepository.update_document_notebook', return_value=True) as mock_update:
        result = notebook_service.update_document_notebook('doc1', 'new note')
        assert result is True
        mock_update.assert_called_once_with('doc1', 'new note')

def test_update_project_notebook(notebook_service):
    with patch('services.notebook_service.NotebookRepository.update_project_notebook', return_value=True) as mock_update:
        result = notebook_service.update_project_notebook('proj1', 'new note')
        assert result is True
        mock_update.assert_called_once_with('proj1', 'new note')

def test_download_documents_notebook(notebook_service):
    with patch.object(notebook_service, 'get_documents_notebook', return_value='doc notes'), \
         patch('services.notebook_service.DocumentRepository.get_by_document_id', return_value={'title': 'DocTitle'}):
        buffer, filename = notebook_service.download_documents_notebook('doc1')
        assert isinstance(buffer, io.BytesIO)
        assert buffer.getvalue() == b'doc notes'
        assert filename == 'DocTitlenotes.txt'

def test_download_projects_notebook(notebook_service):
    with patch.object(notebook_service, 'get_projects_notebook', return_value='proj notes'), \
         patch('services.notebook_service.ProjectRepository.get_project_by_id', return_value={'title': 'ProjTitle'}):
        buffer, filename = notebook_service.download_projects_notebook('proj1')
        assert isinstance(buffer, io.BytesIO)
        assert buffer.getvalue() == b'proj notes'
        assert filename == 'ProjTitlenotes.txt'

def test_validate_note_content_empty(notebook_service):
    # Should not raise
    notebook_service._validate_note_content("")

def test_validate_note_content_max_length(notebook_service):
    InvalidNoteContent.MAX_NOTE_LENGTH = 5
    with pytest.raises(InvalidNoteContent):
        notebook_service._validate_note_content('123456')

def test_get_projects_notebook_notebook_not_found(notebook_service):
    from exceptions.notebook_exceptions import NotebookNotFoundError
    with patch.object(notebook_service.notebook_repository, 'get_project_notebook', return_value=None):
        with pytest.raises(NotebookNotFoundError):
            notebook_service.get_projects_notebook('proj1')

def test_get_documents_notebook_notebook_not_found(notebook_service):
    from exceptions.notebook_exceptions import NotebookNotFoundError
    with patch.object(notebook_service.notebook_repository, 'get_document_notebook', return_value=None):
        with pytest.raises(NotebookNotFoundError):
            notebook_service.get_documents_notebook('doc1')

def test_update_document_notebook_invalid_note(notebook_service):
    from exceptions.notebook_exceptions import InvalidNoteContent
    with patch.object(notebook_service, '_validate_note_content', side_effect=InvalidNoteContent()):
        with pytest.raises(InvalidNoteContent):
            notebook_service.update_document_notebook('doc1', 'bad')

def test_update_project_notebook_invalid_note(notebook_service):
    from exceptions.notebook_exceptions import InvalidNoteContent
    with patch.object(notebook_service, '_validate_note_content', side_effect=InvalidNoteContent()):
        with pytest.raises(InvalidNoteContent):
            notebook_service.update_project_notebook('proj1', 'bad')

def test_update_document_notebook_save_exception(notebook_service):
    from exceptions.notebook_exceptions import NotebookSaveException
    with patch('services.notebook_service.NotebookRepository.update_document_notebook', side_effect=Exception('fail')):
        with pytest.raises(NotebookSaveException):
            notebook_service.update_document_notebook('doc1', 'note')

def test_update_project_notebook_save_exception(notebook_service):
    from exceptions.notebook_exceptions import NotebookSaveException
    with patch('services.notebook_service.NotebookRepository.update_project_notebook', side_effect=Exception('fail')):
        with pytest.raises(NotebookSaveException):
            notebook_service.update_project_notebook('proj1', 'note')

def test_download_documents_notebook_no_title(notebook_service):
    with patch.object(notebook_service, 'get_documents_notebook', return_value='doc notes'), \
         patch('services.notebook_service.DocumentRepository.get_by_document_id', return_value={}):
        buffer, filename = notebook_service.download_documents_notebook('doc1')
        assert filename == 'notes.txt'

def test_download_projects_notebook_no_title(notebook_service):
    with patch.object(notebook_service, 'get_projects_notebook', return_value='proj notes'), \
         patch('services.notebook_service.ProjectRepository.get_project_by_id', return_value={}):
        buffer, filename = notebook_service.download_projects_notebook('proj1')
        assert filename == 'notes.txt'
