import unittest
from unittest.mock import patch, MagicMock
from database.repository.conversation_repository import ConversationRepository
from pymongo.errors import DuplicateKeyError

class TestConversationRepository(unittest.TestCase):
    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_save_new_conversation(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.insert_one.return_value.inserted_id = '12345'
        conversation_data = {'user_id': 'user1', 'name': 'Test Conversation'}
        result = ConversationRepository.save(conversation_data)
        self.assertEqual(result, '12345')
        mock_db.conversations.insert_one.assert_called_once_with(conversation_data)
        mock_es.index.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_save_duplicate_conversation(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.insert_one.side_effect = DuplicateKeyError('duplicate')
        mock_db.conversations.find_one.return_value = {'_id': 'existing_id'}
        conversation_data = {'user_id': 'user1', 'name': 'Test Conversation'}
        result = ConversationRepository.save(conversation_data)
        self.assertEqual(result, 'existing_id')
        mock_db.conversations.find_one.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_get_conversation_by_id(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.find_one.return_value = {'_id': '12345', 'name': 'Test'}
        result = ConversationRepository.get_conversation_by_id('12345')
        self.assertEqual(result['name'], 'Test')
        mock_db.conversations.find_one.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_get_user_conversations(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.find.return_value = [{'_id': '1'}, {'_id': '2'}]
        result = ConversationRepository.get_user_conversations('user1')
        self.assertEqual(len(result), 2)
        mock_db.conversations.find.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_get_conversation_by_name(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.find_one.return_value = {'_id': '123', 'name': 'Test'}
        result = ConversationRepository.get_conversation_by_name('Test')
        self.assertEqual(result['name'], 'Test')
        mock_db.conversations.find_one.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_get_conversation_by_document(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.find_one.return_value = {'_id': '123', 'document_id': 'doc1'}
        result = ConversationRepository.get_conversation_by_document('doc1')
        self.assertEqual(result['document_id'], 'doc1')
        mock_db.conversations.find_one.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_delete_conversation(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.delete_one.return_value.deleted_count = 1
        mock_es.exists.return_value = True
        result = ConversationRepository.delete_conversation('12345')
        self.assertTrue(result)
        mock_db.conversations.delete_one.assert_called_once()
        mock_es.delete.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_delete_conversation_for_document(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.delete_one.return_value.deleted_count = 1
        result = ConversationRepository.delete_conversation_for_document('doc1')
        self.assertTrue(result)
        mock_db.conversations.delete_one.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_clear_history(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.delete_many.return_value.deleted_count = 2
        mock_es.delete_by_query.return_value = None
        result = ConversationRepository.clear_history('user1')
        self.assertTrue(result)
        mock_db.conversations.delete_many.assert_called_once()
        mock_es.delete_by_query.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_delete_all_conversations(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.delete_many.return_value.deleted_count = 3
        mock_es.delete_by_query.return_value = None
        result = ConversationRepository.delete_all_conversations('user1')
        self.assertTrue(result)
        mock_db.conversations.delete_many.assert_called_once()
        mock_es.delete_by_query.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_update_conversation_name(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.update_one.return_value.modified_count = 1
        mock_es.exists.return_value = True
        result = ConversationRepository.update_conversation_name('123', 'New Name')
        self.assertTrue(result)
        mock_db.conversations.update_one.assert_called_once()
        mock_es.update.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    def test_update_list_of_documents(self, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.update_one.return_value.modified_count = 1
        result = ConversationRepository.update_list_of_documents('123', ['doc1', 'doc2'])
        self.assertTrue(result)
        mock_db.conversations.update_one.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.get_utc_zulu_timestamp')
    def test_update_messages(self, mock_timestamp, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value.__enter__.return_value = mock_db
        mock_db.conversations.update_one.return_value.modified_count = 1
        mock_db.coversations.update_one.return_value = None
        mock_timestamp.return_value = '2025-08-24T00:00:00Z'
        result = ConversationRepository.update_messages('123', ['msg1', 'msg2'])
        self.assertTrue(result)
        mock_db.conversations.update_one.assert_called()
        mock_db.coversations.update_one.assert_called()

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
        result = ConversationRepository.search_conversation('user1', 'Test')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Test1')
        self.assertEqual(result[1]['id'], '2')
        mock_es.indices.refresh.assert_called_once()
        mock_es.search.assert_called_once()

    @patch('database.repository.conversation_repository.mongo_connection')
    @patch('database.repository.conversation_repository.es')
    def test_conversation_exists(self, mock_es, mock_mongo):
        mock_db = MagicMock()
        mock_mongo.return_value = mock_db
        mock_db.conversations.find_one.return_value = {'_id': '123'}
        mock_es.exists.return_value = True
        result = ConversationRepository.conversation_exists('123')
        self.assertTrue(result)
        mock_db.conversations.find_one.assert_called()
        mock_es.exists.assert_called()

if __name__ == '__main__':
    unittest.main()
