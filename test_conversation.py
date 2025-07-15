import unittest
from datetime import datetime
from bson import ObjectId
from database.repository.conversation_repository import ConversationRepository
from database.utils.mongo_connector import mongo_connection

class TestConversationRepository(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
            "_id": str(ObjectId()),
            "user_id": "test_user_123",
            "name": "Test Conversation",
            "messages": [],
            "vector_store": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        ConversationRepository.save(self.sample_data)

    def tearDown(self):
        with mongo_connection() as db:
            db.conversations.delete_many({"user_id": "test_user_123"})

    def test_get_conversation_by_id(self):
        result = ConversationRepository.get_conversation_by_id(self.sample_data["_id"])
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Test Conversation")

    def test_get_conversations_by_user_id(self):
        results = ConversationRepository.get_conversations_by_user_id("test_user_123")
        self.assertIsInstance(results, list)

    def test_update_conversation_name(self):
        updated = ConversationRepository.update_conversation_name(self.sample_data["_id"], "Updated Name")
        self.assertTrue(updated)
        with mongo_connection() as db:
            conv = db.conversations.find_one({"_id": self.sample_data["_id"]})
            self.assertEqual(conv["name"], "Updated Name")

    def test_update_messages(self):
        new_messages = [{"role": "user", "content": "Hello"}]
        updated = ConversationRepository.update_messages(self.sample_data["_id"], new_messages)
        self.assertTrue(updated)
        with mongo_connection() as db:
            conv = db.conversations.find_one({"_id": self.sample_data["_id"]})
            self.assertEqual(conv["messages"], new_messages)

    def test_delete_conversation(self):
        deleted = ConversationRepository.delete_conversation(self.sample_data["_id"])
        self.assertTrue(deleted)
        with mongo_connection() as db:
            self.assertIsNone(db.conversations.find_one({"_id": self.sample_data["_id"]}))

    def test_delete_all_conversations(self):
        deleted = ConversationRepository.delete_all_conversations("test_user_123")
        self.assertTrue(deleted)
        with mongo_connection() as db:
            remaining = db.conversations.count_documents({"user_id": "test_user_123"})
            self.assertEqual(remaining, 0)

if __name__ == '__main__':
    unittest.main()
