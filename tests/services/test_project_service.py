import pytest
from unittest.mock import patch, MagicMock
from services.project_service import ProjectService
from model.document_reader.project import Project as ProjectModel
from exceptions.project_exceptions import ProjectNotFoundError, InvalidProjectName, DuplicateProjectName

@pytest.fixture
def project_service():
    return ProjectService()

@pytest.fixture
def fake_project_dict():
    return {
        'project_name': 'Alpha',
        'user_id': 'user1',
        '_id': 'proj1',
        'note': 'A note',
        'created_at': '2025-08-22T00:00:00Z',
        'updated_at': '2025-08-23T00:00:00Z'
    }

def test_create_project(project_service):
    with patch.object(project_service, '_validate_project_name'), \
         patch.object(project_service.project_repository, 'save', return_value='proj1'), \
         patch.object(project_service.notebook_service, 'update_project_notebook'):
        project = project_service.create_project('user1', 'Alpha')
        assert isinstance(project, ProjectModel)
        assert project.project_name == 'Alpha'
        assert project.id == 'proj1'

def test_get_project_found(project_service, fake_project_dict):
    with patch.object(project_service.project_repository, 'get_project_by_id', return_value=fake_project_dict):
        project = project_service.get_project('proj1')
        assert isinstance(project, ProjectModel)
        assert project.project_name == 'Alpha'

def test_get_project_not_found(project_service):
    with patch.object(project_service.project_repository, 'get_project_by_id', return_value=None):
        project = project_service.get_project('proj1')
        assert project is None

def test_get_user_projects(project_service, fake_project_dict):
    with patch.object(project_service.library_repository, 'get_user_library', return_value=[fake_project_dict]), \
         patch.object(project_service, 'get_project', return_value=ProjectModel.from_dict(fake_project_dict)):
        projects = project_service.get_user_projects('user1')
        assert isinstance(projects, list)
        assert isinstance(projects[0], ProjectModel)

def test_get_user_projects_none(project_service):
    with patch.object(project_service.library_repository, 'get_user_library', return_value=None):
        projects = project_service.get_user_projects('user1')
        assert projects is None

def test_delete_project_with_documents(project_service):
    with patch.object(project_service.document_repository, 'get_documents_by_project', return_value=[{'_id': 'doc1'}]), \
         patch.object(project_service.project_repository, 'get_project_by_id', return_value={'_id': 'proj1'}), \
         patch.object(project_service.document_service, 'delete_document'), \
         patch.object(project_service.project_repository, 'delete_project', return_value=True):
        result = project_service.delete_project('proj1')
        assert result is True

def test_delete_project_no_documents(project_service):
    with patch.object(project_service.document_repository, 'get_documents_by_project', return_value=None), \
         patch.object(project_service.project_repository, 'get_project_by_id', return_value={'_id': 'proj1'}), \
         patch.object(project_service.project_repository, 'delete_project', return_value=True):
        result = project_service.delete_project('proj1')
        assert result is None

def test_rename_project_success(project_service, fake_project_dict):
    with patch.object(project_service, 'get_project', return_value=ProjectModel.from_dict(fake_project_dict)), \
         patch.object(project_service, '_validate_project_name'), \
         patch.object(project_service.project_repository, 'update_name', return_value=True):
        result = project_service.rename_project('proj1', 'Beta')
        assert result is True

def test_rename_project_not_found(project_service):
    with patch.object(project_service, 'get_project', return_value=None):
        with pytest.raises(ProjectNotFoundError):
            project_service.rename_project('proj1', 'Beta')

def test_sort_project_documents(project_service):
    doc1 = MagicMock()
    doc1.name = 'B'
    doc1.created_at = '2025-08-23T00:00:00Z'
    doc1.document_id = 'doc1'

    doc2 = MagicMock()
    doc2.name = 'A'
    doc2.created_at = '2025-08-22T00:00:00Z'
    doc2.document_id = 'doc2'
    with patch.object(project_service.document_service, 'get_project_documents', return_value=[doc1, doc2]), \
         patch.object(project_service.document_repository, 'get_authors', return_value='author'), \
         patch.object(project_service.document_repository, 'get_year', return_value='2025'), \
         patch.object(project_service.document_repository, 'get_source', return_value='source'):
        sorted_docs = project_service.sort_project_documents('proj1', 'title', 'asc')
        assert sorted_docs[0].name == 'A'
        sorted_docs = project_service.sort_project_documents('proj1', 'created_at', 'desc')
        assert sorted_docs[0].created_at == '2025-08-23T00:00:00Z'

def test_sort_project_documents_invalid_field(project_service):
    doc1 = MagicMock(name='A', document_id='doc1')
    with patch.object(project_service.document_service, 'get_project_documents', return_value=[doc1]):
        with pytest.raises(ValueError):
            project_service.sort_project_documents('proj1', 'invalid', 'asc')

def test_validate_project_name_empty(project_service):
    with pytest.raises(InvalidProjectName):
        project_service._validate_project_name('', 'user1')

def test_validate_project_name_duplicate(project_service, fake_project_dict):
    project = ProjectModel.from_dict(fake_project_dict)
    with patch.object(project_service, 'get_user_projects', return_value=[project]):
        with pytest.raises(DuplicateProjectName):
            project_service._validate_project_name('Alpha', 'user1')
