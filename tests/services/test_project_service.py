import unittest
from unittest.mock import MagicMock
from services.project_service import ProjectService
from model.document_reader.project import Project


class TestProjectService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = ProjectService()
        self.service.project_repository = self.mock_repo  # override with mock

    def test_create_project(self):
        # Arrange
        self.mock_repo.new_project.return_value = 1

        # Act
        result = self.service.create_project(user_id=101, name="Test Project")

        # Assert
        self.assertIsInstance(result, Project)
        self.assertEqual(result.name, "Test Project")
        self.assertEqual(result.user_id, 101)
        self.assertEqual(result.id, 1)
        self.mock_repo.new_project.assert_called_once()

    def test_get_project_found(self):
        # Arrange
        self.mock_repo.get_by_id.return_value = {
            'project_id': 1,
            'name': 'My Project',
            'user_id': 101,
            'note': 'Test note'
        }

        # Act
        result = self.service.get_project(project_id=1)

        # Assert
        self.assertEqual(result.name, 'My Project')
        self.assertEqual(result.id, 1)
        self.assertEqual(result.user_id, 101)
        self.assertEqual(result.note, 'Test note')

    def test_get_project_not_found(self):
        self.mock_repo.get_by_id.return_value = None
        result = self.service.get_project(project_id=999)
        self.assertIsNone(result)

    def test_rename_project_success(self):
        self.mock_repo.update_name.return_value = 1
        result = self.service.rename_project(project_id=1, name="Renamed")
        self.assertTrue(result)

    def test_rename_project_fail(self):
        self.mock_repo.update_name.return_value = 0
        result = self.service.rename_project(project_id=1, name="Renamed")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
