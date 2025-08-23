import pytest
from unittest.mock import patch, MagicMock
from services.notebook_service import NotebookService
import io

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
         patch('services.notebook_service.ProjectRepository.get_by_project_id', return_value={'title': 'ProjTitle'}):
        buffer, filename = notebook_service.download_projects_notebook('proj1')
        assert isinstance(buffer, io.BytesIO)
        assert buffer.getvalue() == b'proj notes'
        assert filename == 'ProjTitlenotes.txt'
