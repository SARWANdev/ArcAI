import pytest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace

# Patch ConversationRepository before importing ConversationService
patcher = patch('services.conversation_service.ConversationRepository', MagicMock())
patcher.start()

from services.conversation_service import ConversationService
from exceptions.base_exceptions import NotFoundException

@pytest.fixture
def service():
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

def test_create_document_conversation_not_found(service):
    with patch('services.document_service.DocumentService.get_document', return_value=None), \
         patch.object(service.conversation_repository, 'save') as mock_save:
        result = service.create_document_conversation('user1', 'doc1')
        assert result is None
        mock_save.assert_not_called()

def test_sort_history_by_name(service):
    data = [{'name': 'B'}, {'name': 'A'}]
    with patch.object(service.conversation_repository, 'get_user_conversations', return_value=data), \
         patch('model.ai_chat.conversation.Conversation.from_dict', side_effect=lambda d: SimpleNamespace(**d)):
        result = service.sort_history('user1', 'name', 'asc')
        assert [c.name for c in result] == ['A', 'B']

def test_sort_history_by_created(service):
    data = [{'created_at': '2'}, {'created_at': '1'}]
    with patch.object(service.conversation_repository, 'get_user_conversations', return_value=data), \
         patch('model.ai_chat.conversation.Conversation.from_dict', side_effect=lambda d: SimpleNamespace(**d)):
        result = service.sort_history('user1', 'created', 'asc')
        assert [c.created_at for c in result] == ['1', '2']

def test_sort_history_invalid(service):
    with patch.object(service.conversation_repository, 'get_user_conversations', return_value=[{'name': 'A'}]):
        with pytest.raises(ValueError):
            service.sort_history('user1', 'invalid', 'asc')

def test_get_conversation_history(service, fake_conversation_dict):
    with patch.object(service.conversation_repository, 'get_user_conversations', return_value=[fake_conversation_dict]), \
         patch('model.ai_chat.conversation.Conversation.from_dict', side_effect=lambda d: SimpleNamespace(**d)):
        history = service.get_conversation_history('user1')
        assert len(history) == 1
        assert history[0].name == 'Test Conversation'

def test_get_conversation_history_empty(service):
    with patch.object(service.conversation_repository, 'get_user_conversations', return_value=[]):
        history = service.get_conversation_history('user1')
        assert history == []

def test_get_conversation(service, fake_conversation_dict):
    with patch.object(service.conversation_repository, 'get_conversation_by_id', return_value=fake_conversation_dict), \
         patch('model.ai_chat.conversation.Conversation.from_dict', side_effect=lambda d: SimpleNamespace(**d)):
        conv = service.get_conversation('cid')
        assert conv.name == 'Test Conversation'

def test_get_conversation_not_found(service):
    with patch.object(service.conversation_repository, 'get_conversation_by_id', return_value=None):
        conv = service.get_conversation('cid')
        assert conv is None

def test_get_conversation_by_document_id(service, fake_conversation_dict):
    with patch.object(service.conversation_repository, 'get_conversation_by_document', return_value=fake_conversation_dict), \
         patch('model.ai_chat.conversation.Conversation.from_dict', side_effect=lambda d: SimpleNamespace(**d)):
        conv = service.get_conversation_by_document_id('docid')
        assert conv.name == 'Test Conversation'

def test_get_conversation_by_document_id_not_found(service):
    with patch.object(service.conversation_repository, 'get_conversation_by_document', return_value=None):
        conv = service.get_conversation_by_document_id('docid')
        assert conv is None

def test_update_messages(service):
    with patch.object(service.conversation_repository, 'update_messages') as mock_update:
        service.update_messages('cid', ['msg1', 'msg2'])
        mock_update.assert_called_once_with(conversation_id='cid', messages=['msg1', 'msg2'])

def test_update_name(service):
    with patch.object(service.conversation_repository, 'update_conversation_name', return_value=True) as mock_update:
        result = service.update_name('cid', 'newname')
        assert result is True
        mock_update.assert_called_once_with(conversation_id='cid', new_name='newname')

def test_rename_chat_success(service):
    with patch.object(service, 'get_conversation', return_value=SimpleNamespace(user_id='user1', name='Old', conversation_id='cid')), \
         patch.object(service, '_validate_conversation_name'), \
         patch.object(service, 'update_name', return_value=True) as mock_update:
        result = service.rename_chat('cid', 'newname')
        assert result is True
        mock_update.assert_called_once_with('cid', 'newname')

def test_rename_chat_not_found(service):
    with patch.object(service, 'get_conversation', return_value=None):
        with pytest.raises(NotFoundException):
            service.rename_chat('badid', 'newname')

def test_delete_chat(service):
    with patch.object(service.conversation_repository, 'delete_conversation') as mock_delete:
        service.delete_chat('cid')
        mock_delete.assert_called_once_with('cid')

def test_clear_history(service):
    with patch.object(service.conversation_repository, 'clear_history') as mock_clear:
        service.clear_history('user1')
        mock_clear.assert_called_once_with('user1')

def test_delete_all_conversations(service):
    with patch.object(service.conversation_repository, 'delete_all_conversations') as mock_delete_all:
        service.delete_all_conversations('user1')
        mock_delete_all.assert_called_once_with('user1')

def test_search_conversations(service):
    with patch.object(service.conversation_repository, 'search_conversation', return_value=[{'id': 'conv1'}]), \
         patch.object(service.conversation_repository, 'get_conversation_by_id', return_value={'id': 'conv1'}), \
         patch('model.ai_chat.conversation.Conversation.from_dict', return_value=SimpleNamespace(get_document_id=lambda: None)):
        result = service.search_conversations('user1', 'query')
        assert isinstance(result, list)
    with patch.object(service.conversation_repository, 'search_conversation', return_value=None):
        result = service.search_conversations('user1', 'query')
        assert result == []

def test_validate_conversation_name_empty(service):
    class DummyInvalid(Exception):
        MAX_NAME_LENGTH = 100
        MIN_NAME_LENGTH = 1
    with patch('exceptions.base_exceptions.InvalidNameException', DummyInvalid):
        with pytest.raises(DummyInvalid):
            service._validate_conversation_name('', 'user1', None)

def test_validate_conversation_name_too_long(service):
    class DummyInvalid(Exception):
        MAX_NAME_LENGTH = 5
        MIN_NAME_LENGTH = 1
    with patch('exceptions.base_exceptions.InvalidNameException', DummyInvalid):
        with pytest.raises(DummyInvalid):
            service._validate_conversation_name('toolongname', 'user1', None)

def test_validate_conversation_name_too_short(service):
    class DummyInvalid(Exception):
        MAX_NAME_LENGTH = 100
        MIN_NAME_LENGTH = 5
    with patch('exceptions.base_exceptions.InvalidNameException', DummyInvalid):
        with pytest.raises(DummyInvalid):
            service._validate_conversation_name('abc', 'user1', None)

def test_validate_conversation_name_duplicate(service):
    class DummyInvalid(Exception):
        MAX_NAME_LENGTH = 100
        MIN_NAME_LENGTH = 1
    class DummyDuplicate(Exception):
        pass
    dup = SimpleNamespace(name="DupName", conversation_id="id1")
    with patch('exceptions.base_exceptions.InvalidNameException', DummyInvalid), \
         patch('exceptions.base_exceptions.DuplicateNameException', DummyDuplicate):
        service.get_conversation_history = lambda user_id: [dup]
        with pytest.raises(DummyDuplicate):
            service._validate_conversation_name("DupName", "user1", "id2")

def test_validate_conversation_name_allows_same_id(service):
    class DummyInvalid(Exception):
        MAX_NAME_LENGTH = 100
        MIN_NAME_LENGTH = 1
    class DummyDuplicate(Exception):
        pass
    dup = SimpleNamespace(name="DupName", conversation_id="id1")
    with patch('exceptions.base_exceptions.InvalidNameException', DummyInvalid), \
         patch('exceptions.base_exceptions.DuplicateNameException', DummyDuplicate):
        service.get_conversation_history = lambda user_id: [dup]
        service._validate_conversation_name("DupName", "user1", "id1")
