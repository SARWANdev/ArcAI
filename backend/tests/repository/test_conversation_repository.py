import unittest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from database.repository.conversation_repository import ConversationRepository
from pymongo.errors import DuplicateKeyError

FAKE_CONVERSATION_ID = "64b2fae99a8b5c5f12345678"
FAKE_USER_ID = "user123"
FAKE_DOCUMENT_ID = "64b2fae99a8b5c5f87654321"

class TestConversationRepository(unittest.TestCase):
    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_save_new_conversation(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.insert_one.return_value.inserted_id = ObjectId(FAKE_CONVERSATION_ID)
        conversation_data = {'user_id': FAKE_USER_ID, 'name': 'Test Conversation'}
        result = ConversationRepository.save(conversation_data)
        self.assertEqual(result, FAKE_CONVERSATION_ID)
        mock_db.conversations.insert_one.assert_called_once_with(conversation_data)
        mock_es.index.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_save_duplicate_conversation(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.insert_one.side_effect = DuplicateKeyError('duplicate')
        mock_db.conversations.find_one.return_value = {'_id': ObjectId(FAKE_CONVERSATION_ID)}
        conversation_data = {'user_id': FAKE_USER_ID, 'name': 'Test Conversation'}
        result = ConversationRepository.save(conversation_data)
        self.assertEqual(result, FAKE_CONVERSATION_ID)
        mock_db.conversations.find_one.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_save_duplicate_conversation_no_existing(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.insert_one.side_effect = DuplicateKeyError('duplicate')
        mock_db.conversations.find_one.return_value = None
        conversation_data = {'user_id': FAKE_USER_ID, 'name': 'Test Conversation'}
        result = ConversationRepository.save(conversation_data)
        self.assertIsNone(result)
        mock_db.conversations.find_one.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_get_conversation_by_id(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.find_one.return_value = {'_id': ObjectId(FAKE_CONVERSATION_ID), 'name': 'Test'}
        result = ConversationRepository.get_conversation_by_id(FAKE_CONVERSATION_ID)
        self.assertEqual(result['name'], 'Test')
        mock_db.conversations.find_one.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_get_user_conversations(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.find.return_value = [{'_id': '1'}, {'_id': '2'}]
        result = ConversationRepository.get_user_conversations(FAKE_USER_ID)
        self.assertEqual(len(result), 2)
        mock_db.conversations.find.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_get_conversation_by_name(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.find_one.return_value = {'_id': ObjectId(FAKE_CONVERSATION_ID), 'name': 'Test'}
        result = ConversationRepository.get_conversation_by_name('Test')
        self.assertEqual(result['name'], 'Test')
        mock_db.conversations.find_one.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_get_conversation_by_document(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.find_one.return_value = {'_id': ObjectId(FAKE_CONVERSATION_ID), 'document_id': FAKE_DOCUMENT_ID}
        result = ConversationRepository.get_conversation_by_document(FAKE_DOCUMENT_ID)
        self.assertEqual(result['document_id'], FAKE_DOCUMENT_ID)
        mock_db.conversations.find_one.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_delete_conversation(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.delete_one.return_value.deleted_count = 1
        mock_es.exists.return_value = True
        result = ConversationRepository.delete_conversation(FAKE_CONVERSATION_ID)
        self.assertTrue(result)
        mock_db.conversations.delete_one.assert_called_once()
        mock_es.delete.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_delete_conversation_es_not_exists(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.delete_one.return_value.deleted_count = 1
        mock_es.exists.return_value = False
        result = ConversationRepository.delete_conversation(FAKE_CONVERSATION_ID)
        self.assertTrue(result)
        mock_db.conversations.delete_one.assert_called_once()
        mock_es.delete.assert_not_called()

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_delete_conversation_exception(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.delete_one.side_effect = Exception("Database error")
        result = ConversationRepository.delete_conversation(FAKE_CONVERSATION_ID)
        self.assertFalse(result)

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_delete_conversation_for_document(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.delete_one.return_value.deleted_count = 1
        result = ConversationRepository.delete_conversation_for_document(FAKE_DOCUMENT_ID)
        self.assertTrue(result)
        mock_db.conversations.delete_one.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_delete_conversation_for_document_exception(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.delete_one.side_effect = Exception("Database error")
        result = ConversationRepository.delete_conversation_for_document(FAKE_DOCUMENT_ID)
        self.assertFalse(result)

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_clear_history(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.delete_many.return_value.deleted_count = 2
        mock_es.delete_by_query.return_value = None
        result = ConversationRepository.clear_history(FAKE_USER_ID)
        self.assertTrue(result)
        mock_db.conversations.delete_many.assert_called_once()
        mock_es.delete_by_query.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_clear_history_exception(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.delete_many.side_effect = Exception("Database error")
        result = ConversationRepository.clear_history(FAKE_USER_ID)
        self.assertFalse(result)

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_delete_all_conversations(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.delete_many.return_value.deleted_count = 3
        mock_es.delete_by_query.return_value = None
        result = ConversationRepository.delete_all_conversations(FAKE_USER_ID)
        self.assertTrue(result)
        mock_db.conversations.delete_many.assert_called_once()
        mock_es.delete_by_query.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_delete_all_conversations_exception(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.delete_many.side_effect = Exception("Database error")
        result = ConversationRepository.delete_all_conversations(FAKE_USER_ID)
        self.assertFalse(result)

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_update_conversation_name(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.update_one.return_value.modified_count = 1
        mock_es.exists.return_value = True
        result = ConversationRepository.update_conversation_name(FAKE_CONVERSATION_ID, 'New Name')
        self.assertTrue(result)
        mock_db.conversations.update_one.assert_called_once()
        mock_es.update.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_update_conversation_name_es_not_exists(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.update_one.return_value.modified_count = 1
        mock_es.exists.return_value = False
        result = ConversationRepository.update_conversation_name(FAKE_CONVERSATION_ID, 'New Name')
        self.assertTrue(result)
        mock_db.conversations.update_one.assert_called_once()
        mock_es.update.assert_not_called()

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_update_conversation_name_exception(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.update_one.side_effect = Exception("Database error")
        result = ConversationRepository.update_conversation_name(FAKE_CONVERSATION_ID, 'New Name')
        self.assertFalse(result)

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_update_list_of_documents(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.update_one.return_value.modified_count = 1
        result = ConversationRepository.update_list_of_documents(FAKE_CONVERSATION_ID, ['doc1', 'doc2'])
        self.assertTrue(result)
        mock_db.conversations.update_one.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_update_list_of_documents_exception(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.update_one.side_effect = Exception("Database error")
        result = ConversationRepository.update_list_of_documents(FAKE_CONVERSATION_ID, ['doc1', 'doc2'])
        self.assertFalse(result)

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.get_utc_zulu_timestamp')
    def test_update_messages(self, mock_timestamp, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.update_one.return_value.modified_count = 1
        mock_db.coversations.update_one.return_value = None
        mock_timestamp.return_value = '2025-08-24T00:00:00Z'
        result = ConversationRepository.update_messages(FAKE_CONVERSATION_ID, ['msg1', 'msg2'])
        self.assertTrue(result)
        mock_db.conversations.update_one.assert_called()
        mock_db.coversations.update_one.assert_called()

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.get_utc_zulu_timestamp')
    def test_update_messages_exception(self, mock_timestamp, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.update_one.side_effect = Exception("Database error")
        result = ConversationRepository.update_messages(FAKE_CONVERSATION_ID, ['msg1', 'msg2'])
        self.assertFalse(result)

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.get_utc_zulu_timestamp')
    def test_update_messages_coversations_exception(self, mock_timestamp, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.update_one.return_value.modified_count = 1
        mock_db.coversations.update_one.side_effect = Exception("Typo in collection name")
        result = ConversationRepository.update_messages(FAKE_CONVERSATION_ID, ['msg1', 'msg2'])
        self.assertFalse(result)

    @patch('database.repository.conversation_repository.es')
    def test_search_conversation(self, mock_es):
        mock_es.indices.refresh.return_value = None
        mock_es.search.return_value = {
            'hits': {
                'hits': [
                    {'_id': '1', '_source': {'name': 'Test1'}},
                    {'_id': '2', '_source': {'name': 'Test2'}}
                ]
            }
        }
        result = ConversationRepository.search_conversation(FAKE_USER_ID, 'Test')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Test1')
        self.assertEqual(result[1]['id'], '2')
        mock_es.indices.refresh.assert_called_once()
        mock_es.search.assert_called_once()

    @patch('database.repository.conversation_repository.es')
    def test_add_to_es(self, mock_es):
        ConversationRepository.add_to_es(FAKE_CONVERSATION_ID, 'Test Conversation', FAKE_USER_ID)
        mock_es.index.assert_called_once_with(
            index="conversations", 
            id=FAKE_CONVERSATION_ID, 
            body={
                "user_id": FAKE_USER_ID,
                "name": 'Test Conversation',
                "suggest": {"input": 'Test Conversation'}
            }
        )

if __name__ == '__main__':
    unittest.main()
