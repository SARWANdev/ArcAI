import unittest
from datetime import datetime, timezone
from bson import ObjectId
from database.repository.conversation_repository import ConversationRepository
from database.utils.mongo_connector import mongo_connection
from database.utils.db_setup import es


class TestConversationRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):    
        cls.clean_conversations_index(user_ids=["test_user_1", "user_id_1"])

    @staticmethod
    def clean_conversations_index(user_ids=("test_user_1", "user_id_1")):
        if es.indices.exists(index="conversations"):
            for uid in user_ids:
                es.delete_by_query(
                    index="conversations",
                    body={"query": {"term": {"user_id": uid}}},
                    conflicts="proceed"
                )
    
    def setUp(self):
        self.user_id_1 = "test_user_1"
        self.user_id_2 = "test_user_2"

        self.chat_1 = {
            "_id": str(ObjectId()),
            "user_id": self.user_id_1,
            "name": "Conversation 1",
            "messages": [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        self.chat_2 = {
            "_id": str(ObjectId()),
            "user_id": self.user_id_2,
            "name": "Conversation 2",
            "messages": [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        self.chat_3 = {
            "_id": str(ObjectId()),
            "user_id": self.user_id_1,
            "name": "Conversation 3",
            "messages": [],
            "vector_store": None,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }

        
    
"""""
        # Insert test data
        ConversationRepository.save(self.chat_1)
        ConversationRepository.add_to_history(self.chat_1)
        ConversationRepository.save(self.chat_2)
        ConversationRepository.save(self.chat_3)

    def tearDown(self):
        with mongo_connection() as db:
            if es.indices.exists(index="conversations"):
                es.indices.delete(index="conversations")
                es.indices.create(index="conversations")
            db.conversations.delete_many({"user_id": self.user_id_1})
            db.conversations.delete_many({"user_id": self.user_id_2})

    def test_get_conversation_by_id(self):
        result = ConversationRepository.get_conversation_by_id(self.chat_1["_id"])
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], self.chat_1["name"])

    def test_get_conversations_by_user_id(self):
        results = ConversationRepository.get_conversations_by_user_id(self.user_id_1)
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 1)
        for r in results:
            self.assertEqual(r["user_id"], self.user_id_1)

    def test_update_conversation_name(self):
        new_name = "Updated Name"
        updated = ConversationRepository.update_conversation_name(self.chat_1["_id"], new_name)
        self.assertTrue(updated)
        with mongo_connection() as db:
            conv = db.conversations.find_one({"_id": self.chat_1["_id"]})
            self.assertEqual(conv["name"], new_name)

    def test_update_messages(self):
        new_messages = [{"role": "user", "content": "Hello"}]
        updated = ConversationRepository.update_messages(self.chat_1["_id"], new_messages)
        self.assertTrue(updated)
        with mongo_connection() as db:
            conv = db.conversations.find_one({"_id": self.chat_1["_id"]})
            self.assertEqual(conv["messages"], new_messages)

    def test_delete_conversation(self):
        deleted = ConversationRepository.delete_conversation(self.chat_1["_id"])
        self.assertTrue(deleted)
        with mongo_connection() as db:
            self.assertIsNone(db.conversations.find_one({"_id": self.chat_1["_id"]}))

    def test_delete_all_conversations(self):
        deleted = ConversationRepository.delete_all_conversations(self.user_id_1)
        self.assertTrue(deleted)
        with mongo_connection() as db:
            remaining = db.conversations.count_documents({"user_id": self.user_id_1})
            self.assertEqual(remaining, 0)

    def test_add_to_history_and_search(self):
        success = ConversationRepository.add_to_history(self.chat_3)
        self.assertTrue(success)
        results = ConversationRepository.search_conversation(self.user_id_1, "Conversation 3")
        self.assertTrue(any(hit["name"] == "Conversation 3" for hit in results))

    def test_get_history(self):
        history = ConversationRepository.get_history(self.user_id_1)
        self.assertIsInstance(history, list)
        self.assertTrue(any(doc["name"] == "Conversation 1" for doc in history))
"""""

if __name__ == '__main__':
    unittest.main()
