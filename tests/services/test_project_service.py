import unittest
from unittest.mock import patch, MagicMock
from database.repository.project_repository import Project

class TestProjectRepository(unittest.TestCase):
    @patch("database.repository.project_repository.mongo_connection")
    def test_new_project_inserts_correct_data(self, mock_mongo_connection):
        mock_db = MagicMock()
        mock_projects = MagicMock()
        mock_db.projects = mock_projects
        mock_mongo_connection.return_value.__enter__.return_value = mock_db

        mock_projects.insert_one.return_value.inserted_id = "fake_id"

        repo = Project(user_id=123, project_name="My Project", note="My note")
        result = repo.new_project()

        mock_projects.insert_one.assert_called_once()
        inserted_data = mock_projects.insert_one.call_args[0][0]
        self.assertEqual(inserted_data["user_id"], 123)
        self.assertEqual(inserted_data["project_name"], "My Project")
        self.assertEqual(inserted_data["note"], "My note")
        self.assertEqual(result, "fake_id")

    @patch("database.repository.project_repository.mongo_connection")
    def test_get_project_by_user_id_returns_project(self, mock_mongo_connection):
        mock_db = MagicMock()
        mock_projects = MagicMock()
        mock_db.projects = mock_projects
        mock_mongo_connection.return_value.__enter__.return_value = mock_db

        fake_project = {"_id": "abc123", "user_id": 123}
        mock_projects.find_one.return_value = fake_project

        result = Project.get_project_by_user_id(user_id=123)

        mock_projects.find_one.assert_called_once_with({"user_id": 123})
        self.assertEqual(result, fake_project)

    @patch("database.repository.project_repository.mongo_connection")
    def test_get_project_by_id_returns_project(self, mock_mongo_connection):
        mock_db = MagicMock()
        mock_projects = MagicMock()
        mock_db.projects = mock_projects
        mock_mongo_connection.return_value.__enter__.return_value = mock_db

        fake_project = {"_id": "abc123", "user_id": 123}
        mock_projects.find_one.return_value = fake_project

        result = Project.get_project_by_id(project_id="abc123")

        mock_projects.find_one.assert_called_once_with({"_id": "abc123"})
        self.assertEqual(result, fake_project)

    @patch("database.repository.project_repository.mongo_connection")
    def test_update_name_updates_project_name(self, mock_mongo_connection):
        mock_db = MagicMock()
        mock_projects = MagicMock()
        mock_db.projects = mock_projects
        mock_mongo_connection.return_value.__enter__.return_value = mock_db

        mock_projects.update_one.return_value.modified_count = 1

        Project.update_name(project_id="abc123", new_name="Updated Project")

        mock_projects.update_one.assert_called_once_with(
            {"_id": "abc123"}, {"$set": {"name": "Updated Project"}}
        )

if __name__ == "__main__":
    unittest.main()
