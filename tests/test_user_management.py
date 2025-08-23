import pytest
from unittest.mock import patch, MagicMock
from services.user_management.user_service import UserService
from model.user_profile.user import User as UserModel

@pytest.fixture
def user_service():
    return UserService()

def test_get_user_profile_found(user_service):
    user_data = {'_id': 'user1', 'name': 'Test User'}
    with patch.object(user_service.user_repository, 'get_user_by_id', return_value=user_data):
        with patch('model.user_profile.user.User.from_dict', return_value=MagicMock()):
            user = user_service.get_user_profile('user1')
            assert user is not None

def test_get_user_profile_not_found(user_service):
    with patch.object(user_service.user_repository, 'get_user_by_id', return_value=None):
        user = user_service.get_user_profile('user1')
        assert user is None

def test_remove_user(user_service):
    with patch('services.user_management.user_service.LibraryRepository.get_user_library', return_value=[{'_id': 'proj1'}]), \
         patch.object(user_service.project_service, 'delete_project') as mock_delete_project, \
         patch('services.user_management.user_service.delete_remote_directory') as mock_delete_dir, \
         patch.object(user_service.user_repository, 'deactivate_user') as mock_deactivate, \
         patch.object(user_service.conversation_service, 'delete_all_conversations') as mock_delete_convos:
        user_service.remove_user('user1')
        mock_delete_project.assert_called_once_with('proj1')
        mock_delete_dir.assert_called_once()
        mock_deactivate.assert_called_once_with('user1')
        mock_delete_convos.assert_called_once_with('user1')

def test_get_preference_found(user_service):
    user_data = {'_id': 'user1', 'view_mode': True}
    with patch.object(user_service.user_repository, 'get_user_by_id', return_value=user_data):
        pref = user_service.get_preference('user1')
        assert pref is True

def test_get_preference_not_found(user_service):
    with patch.object(user_service.user_repository, 'get_user_by_id', return_value=None):
        pref = user_service.get_preference('user1')
        assert pref is None

def test_update_preference(user_service):
    with patch.object(user_service.user_repository, 'update_view_mode', return_value=True) as mock_update:
        result = user_service.update_preference('user1', False)
        assert result is True
        mock_update.assert_called_once_with('user1', False)
