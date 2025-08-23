import pytest
from unittest.mock import patch, MagicMock
from services.conversation_service import ConversationService
from model.ai_chat.conversation import Conversation as ConversationModel
from exceptions.conversation_exceptions import ConversationNotFoundError

@pytest.fixture
def conversation_service():
    return ConversationService()

@pytest.fixture
def fake_conversation_dict():
    return {
        'name': 'Test Conversation',
        'user_id': 'user1',
        'document_ids': ['doc1'],
        'project_ids': ['proj1'],
        'conversation_id': 'conv1',
        'created_at': '2025-08-23T00:00:00Z',
        'updated_at': '2025-08-23T00:00:00Z'
    }

def test_create_conversation(conversation_service):
    with patch.object(conversation_service.conversation_repository, 'save') as mock_save:
        conv = conversation_service.create_conversation('user1', ['doc1'], ['proj1'], 'Test Conversation')
        assert isinstance(conv, ConversationModel)
        mock_save.assert_called_once()

def test_get_conversation_history(conversation_service, fake_conversation_dict):
    with patch.object(conversation_service.conversation_repository, 'get_user_conversations', return_value=[fake_conversation_dict]):
        history = conversation_service.get_conversation_history('user1')
        assert len(history) == 1
        assert isinstance(history[0], ConversationModel)

def test_get_conversation_not_found(conversation_service):
    with patch.object(conversation_service.conversation_repository, 'get_conversation_by_id', return_value=None):
        result = conversation_service.get_conversation('notfound')
        assert result is None

def test_rename_chat_not_found(conversation_service):
    with patch.object(conversation_service, 'get_conversation', return_value=None):
        with pytest.raises(ConversationNotFoundError):
            conversation_service.rename_chat('badid', 'newname')

def test_create_document_conversation_found(conversation_service):
    with patch('services.conversation_service.DocumentService.get_document', return_value=MagicMock(name='DocName')):
        with patch.object(conversation_service.conversation_repository, 'save') as mock_save:
            result = conversation_service.create_document_conversation('user1', 'doc1')
            assert result is not None
            mock_save.assert_called_once()

def test_create_document_conversation_not_found(conversation_service):
    with patch('services.conversation_service.DocumentService.get_document', return_value=None):
        result = conversation_service.create_document_conversation('user1', 'doc1')
        assert result is None

def test_sort_history_by_name(conversation_service):
    data = [{'name': 'B'}, {'name': 'A'}]
    with patch.object(conversation_service.conversation_repository, 'get_user_conversations', return_value=data):
        result = conversation_service.sort_history('user1', 'name', 'asc')
        assert [c.name for c in result] == ['A', 'B']

def test_sort_history_by_created(conversation_service):
    data = [{'created_at': '2'}, {'created_at': '1'}]
    with patch.object(conversation_service.conversation_repository, 'get_user_conversations', return_value=data):
        result = conversation_service.sort_history('user1', 'created', 'asc')
        assert [c.created_at for c in result] == ['1', '2']

def test_sort_history_invalid(conversation_service):
    with patch.object(conversation_service.conversation_repository, 'get_user_conversations', return_value=[{'name': 'A'}]):
        with pytest.raises(ValueError):
            conversation_service.sort_history('user1', 'invalid', 'asc')

def test_update_messages(conversation_service):
    with patch.object(conversation_service.conversation_repository, 'update_messages') as mock_update:
        conversation_service.update_messages('conv1', ['msg1', 'msg2'])
        mock_update.assert_called_once_with(conversation_id='conv1', messages=['msg1', 'msg2'])

def test_update_name(conversation_service):
    with patch.object(conversation_service.conversation_repository, 'update_conversation_name', return_value=True) as mock_update:
        result = conversation_service.update_name('conv1', 'newname')
        assert result is True
        mock_update.assert_called_once_with(conversation_id='conv1', new_name='newname')

def test_delete_chat(conversation_service):
    with patch.object(conversation_service.conversation_repository, 'delete_conversation') as mock_delete:
        conversation_service.delete_chat('conv1')
        mock_delete.assert_called_once_with('conv1')

def test_clear_history(conversation_service):
    with patch.object(conversation_service.conversation_repository, 'clear_history') as mock_clear:
        conversation_service.clear_history('user1')
        mock_clear.assert_called_once_with('user1')

def test_delete_all_conversations(conversation_service):
    with patch.object(conversation_service.conversation_repository, 'delete_all_conversations') as mock_delete_all:
        conversation_service.delete_all_conversations('user1')
        mock_delete_all.assert_called_once_with('user1')

def test_search_conversations(conversation_service):
    with patch.object(conversation_service.conversation_repository, 'search_conversation', return_value=[{'id': 'conv1'}]), \
         patch.object(conversation_service.conversation_repository, 'get_conversation_by_id', return_value={'id': 'conv1'}), \
         patch('model.ai_chat.conversation.Conversation.from_dict', return_value=MagicMock(get_document_id=MagicMock(return_value=None))):
        result = conversation_service.search_conversations('user1', 'query')
        assert isinstance(result, list)
    with patch.object(conversation_service.conversation_repository, 'search_conversation', return_value=None):
        result = conversation_service.search_conversations('user1', 'query')
        assert result == []
