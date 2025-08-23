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
