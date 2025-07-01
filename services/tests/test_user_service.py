import unittest
from unittest.mock import patch, MagicMock
from services.user_management.user_service import UserService
from model.user_profile.user import User as UserModel

 
class TestUserService(unittest.TestCase):

    def setUp(self):
        self.user_service = UserService()
        self.mock_user_data = {
            "user_id": "123",
            "first_name": "Alice",
            "last_name": "Doe",
            "email": "alice@example.com",
            "preferred_mode": "dark"
        }

    @patch('database.repository.user_repository.User.get_user_by_id')
    def test_get_user_profile_success(self, mock_get_user_by_id):
        # Arrange
        mock_get_user_by_id.return_value = self.mock_user_data

        # Act
        result = self.user_service.get_user_profile("123")

        # Assert
        self.assertIsInstance(result, UserModel)
        self.assertEqual(result.user_id, "123")
        self.assertEqual(result.first_name, "Alice")
        self.assertEqual(result.last_name, "Doe")
        self.assertEqual(result.email, "alice@example.com")
        self.assertEqual(result.prefered_mode, "dark")

    @patch('database.repository.user_repository.User.get_user_by_id')
    def test_get_user_profile_not_found(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = None
        result = self.user_service.get_user_profile("999")
        self.assertIsNone(result)

    
    @patch('database.repository.user_repository.User.get_user_by_id')
    def test_get_preference_success(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = self.mock_user_data
        result = self.user_service.get_preference("123")
        self.assertEqual(result, "dark")

    @patch('database.repository.user_repository.User.get_user_by_id')
    def test_get_preference_user_not_found(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = None
        result = self.user_service.get_preference("404")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
