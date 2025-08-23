import pytest
from unittest.mock import patch, MagicMock
from services.library_service import LibraryService
from model.document_reader.project import Project

@pytest.fixture
def library_service():
    return LibraryService()

@pytest.fixture
def fake_project_dict():
    return {
        'project_name': 'Alpha',
        'created_at': '2025-08-22T00:00:00Z',
        'updated_at': '2025-08-23T00:00:00Z',
        'note': 'A note'
    }

def test_sort_library_by_name(library_service, fake_project_dict):
    with patch.object(library_service.library_repository, 'get_user_library', return_value=[fake_project_dict]):
        projects = library_service.sort_library('user1', 'name', 'asc')
        assert len(projects) == 1
        assert isinstance(projects[0], Project)
        assert projects[0].project_name == 'Alpha'
        assert projects[0].note == 'A note'

def test_sort_library_by_created(library_service, fake_project_dict):
    with patch.object(library_service.library_repository, 'get_user_library', return_value=[fake_project_dict]):
        projects = library_service.sort_library('user1', 'created', 'asc')
        assert len(projects) == 1
        assert projects[0].created_at == '2025-08-22T00:00:00Z'

def test_sort_library_by_updated(library_service, fake_project_dict):
    with patch.object(library_service.library_repository, 'get_user_library', return_value=[fake_project_dict]):
        projects = library_service.sort_library('user1', 'updated', 'asc')
        assert len(projects) == 1
        assert projects[0].updated_at == '2025-08-23T00:00:00Z'

def test_sort_library_empty(library_service):
    with patch.object(library_service.library_repository, 'get_user_library', return_value=None):
        projects = library_service.sort_library('user1', 'name', 'asc')
        assert projects == []

def test_sort_library_invalid_sort_by(library_service, fake_project_dict):
    with patch.object(library_service.library_repository, 'get_user_library', return_value=[fake_project_dict]):
        with pytest.raises(ValueError):
            library_service.sort_library('user1', 'invalid', 'asc')
