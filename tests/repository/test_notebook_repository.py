import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from database.repository.notebook_repository import Notebook

FAKE_PROJECT_ID = "64b2fae99a8b5c5f12345678"
FAKE_DOCUMENT_ID = "64b2fae99a8b5c5f87654321"
FAKE_NOTE = "This is a test notebook content"
FAKE_PROJECT = {
    "_id": ObjectId(FAKE_PROJECT_ID),
    "project_name": "Test Project",
    "note": FAKE_NOTE,
    "user_id": "user123"
}
FAKE_DOCUMENT = {
    "_id": ObjectId(FAKE_DOCUMENT_ID),
    "document_name": "Test Document",
    "note": FAKE_NOTE,
    "user_id": "user123"
}


@pytest.fixture
def mock_db():
    """Returns a fake DB connection mock."""
    mock_db = MagicMock()
    mock_db.projects = MagicMock()
    mock_db.documents = MagicMock()
    return mock_db


class TestGetProjectNotebook:
    """Test cases for get_project_notebook method."""

    def test_get_project_notebook_success(self, mock_db):
        """Test successful project notebook retrieval."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.projects.find_one.return_value = FAKE_PROJECT

            result = Notebook.get_project_notebook(FAKE_PROJECT_ID)
            
            assert result == FAKE_NOTE
            mock_db.projects.find_one.assert_called_once_with({"_id": ObjectId(FAKE_PROJECT_ID)})

    def test_get_project_notebook_not_found(self, mock_db):
        """Test project notebook retrieval when project doesn't exist."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.projects.find_one.return_value = None

            result = Notebook.get_project_notebook(FAKE_PROJECT_ID)
            
            assert result == ""
            mock_db.projects.find_one.assert_called_once_with({"_id": ObjectId(FAKE_PROJECT_ID)})

    def test_get_project_notebook_no_note_field(self, mock_db):
        """Test project notebook retrieval when project exists but has no note field."""
        project_without_note = {
            "_id": ObjectId(FAKE_PROJECT_ID),
            "project_name": "Test Project",
            "user_id": "user123"
            # No note field
        }
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.projects.find_one.return_value = project_without_note

            result = Notebook.get_project_notebook(FAKE_PROJECT_ID)
            
            assert result == ""
            mock_db.projects.find_one.assert_called_once_with({"_id": ObjectId(FAKE_PROJECT_ID)})

    def test_get_project_notebook_exception(self, mock_db):
        """Test project notebook retrieval with database exception."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.projects.find_one.side_effect = Exception("Database error")

            result = Notebook.get_project_notebook(FAKE_PROJECT_ID)
            
            assert result == ""

    def test_get_project_notebook_connection_exception(self, mock_db):
        """Test project notebook retrieval with connection exception."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.side_effect = Exception("Connection failed")

            result = Notebook.get_project_notebook(FAKE_PROJECT_ID)
            
            assert result == ""

    def test_get_project_notebook_invalid_id(self, mock_db):
        """Test project notebook retrieval with invalid ID."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.projects.find_one.side_effect = Exception("Invalid ObjectId")

            result = Notebook.get_project_notebook("invalid_id")
            
            assert result == ""


class TestUpdateProjectNotebook:
    """Test cases for update_project_notebook method."""

    def test_update_project_notebook_success(self, mock_db):
        """Test successful project notebook update."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.projects.update_one.return_value.modified_count = 1

            result = Notebook.update_project_notebook(FAKE_PROJECT_ID, FAKE_NOTE)
            
            assert result is True
            mock_db.projects.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_PROJECT_ID)}, 
                {"$set": {"note": FAKE_NOTE}}
            )

    def test_update_project_notebook_not_found(self, mock_db):
        """Test project notebook update when project doesn't exist."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.projects.update_one.return_value.modified_count = 0

            result = Notebook.update_project_notebook(FAKE_PROJECT_ID, FAKE_NOTE)
            
            assert result is False
            mock_db.projects.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_PROJECT_ID)}, 
                {"$set": {"note": FAKE_NOTE}}
            )

    def test_update_project_notebook_exception(self, mock_db):
        """Test project notebook update with database exception."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.projects.update_one.side_effect = Exception("Database error")

            result = Notebook.update_project_notebook(FAKE_PROJECT_ID, FAKE_NOTE)
            
            assert result is False

    def test_update_project_notebook_connection_exception(self, mock_db):
        """Test project notebook update with connection exception."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.side_effect = Exception("Connection failed")

            result = Notebook.update_project_notebook(FAKE_PROJECT_ID, FAKE_NOTE)
            
            assert result is False

    def test_update_project_notebook_empty_note(self, mock_db):
        """Test project notebook update with empty note."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.projects.update_one.return_value.modified_count = 1

            result = Notebook.update_project_notebook(FAKE_PROJECT_ID, "")
            
            assert result is True
            mock_db.projects.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_PROJECT_ID)}, 
                {"$set": {"note": ""}}
            )

    def test_update_project_notebook_none_note(self, mock_db):
        """Test project notebook update with None note."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.projects.update_one.return_value.modified_count = 1

            result = Notebook.update_project_notebook(FAKE_PROJECT_ID, None)
            
            assert result is True
            mock_db.projects.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_PROJECT_ID)}, 
                {"$set": {"note": None}}
            )


class TestGetDocumentNotebook:
    """Test cases for get_document_notebook method."""

    def test_get_document_notebook_success(self, mock_db):
        """Test successful document notebook retrieval."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.find_one.return_value = FAKE_DOCUMENT

            result = Notebook.get_document_notebook(FAKE_DOCUMENT_ID)
            
            assert result == FAKE_NOTE
            mock_db.documents.find_one.assert_called_once_with({"_id": ObjectId(FAKE_DOCUMENT_ID)})

    def test_get_document_notebook_not_found(self, mock_db):
        """Test document notebook retrieval when document doesn't exist."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.find_one.return_value = None

            result = Notebook.get_document_notebook(FAKE_DOCUMENT_ID)
            
            assert result == ""
            mock_db.documents.find_one.assert_called_once_with({"_id": ObjectId(FAKE_DOCUMENT_ID)})

    def test_get_document_notebook_no_note_field(self, mock_db):
        """Test document notebook retrieval when document exists but has no note field."""
        document_without_note = {
            "_id": ObjectId(FAKE_DOCUMENT_ID),
            "document_name": "Test Document",
            "user_id": "user123"
            # No note field
        }
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.find_one.return_value = document_without_note

            result = Notebook.get_document_notebook(FAKE_DOCUMENT_ID)
            
            assert result == ""
            mock_db.documents.find_one.assert_called_once_with({"_id": ObjectId(FAKE_DOCUMENT_ID)})

    def test_get_document_notebook_exception(self, mock_db):
        """Test document notebook retrieval with database exception."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.find_one.side_effect = Exception("Database error")

            result = Notebook.get_document_notebook(FAKE_DOCUMENT_ID)
            
            assert result == ""

    def test_get_document_notebook_connection_exception(self, mock_db):
        """Test document notebook retrieval with connection exception."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.side_effect = Exception("Connection failed")

            result = Notebook.get_document_notebook(FAKE_DOCUMENT_ID)
            
            assert result == ""

    def test_get_document_notebook_invalid_id(self, mock_db):
        """Test document notebook retrieval with invalid ID."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.find_one.side_effect = Exception("Invalid ObjectId")

            result = Notebook.get_document_notebook("invalid_id")
            
            assert result == ""


class TestUpdateDocumentNotebook:
    """Test cases for update_document_notebook method."""

    def test_update_document_notebook_success(self, mock_db):
        """Test successful document notebook update."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = Notebook.update_document_notebook(FAKE_DOCUMENT_ID, FAKE_NOTE)
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"note": FAKE_NOTE}}
            )

    def test_update_document_notebook_not_found(self, mock_db):
        """Test document notebook update when document doesn't exist."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 0

            result = Notebook.update_document_notebook(FAKE_DOCUMENT_ID, FAKE_NOTE)
            
            assert result is False
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"note": FAKE_NOTE}}
            )

    def test_update_document_notebook_exception(self, mock_db):
        """Test document notebook update with database exception."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.side_effect = Exception("Database error")

            result = Notebook.update_document_notebook(FAKE_DOCUMENT_ID, FAKE_NOTE)
            
            assert result is False

    def test_update_document_notebook_connection_exception(self, mock_db):
        """Test document notebook update with connection exception."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.side_effect = Exception("Connection failed")

            result = Notebook.update_document_notebook(FAKE_DOCUMENT_ID, FAKE_NOTE)
            
            assert result is False

    def test_update_document_notebook_empty_note(self, mock_db):
        """Test document notebook update with empty note."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = Notebook.update_document_notebook(FAKE_DOCUMENT_ID, "")
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"note": ""}}
            )

    def test_update_document_notebook_none_note(self, mock_db):
        """Test document notebook update with None note."""
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = Notebook.update_document_notebook(FAKE_DOCUMENT_ID, None)
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"note": None}}
            )

    def test_update_document_notebook_large_note(self, mock_db):
        """Test document notebook update with large note content."""
        large_note = "A" * 10000  # 10KB note
        with patch("database.repository.notebook_repository.mongo_connection") as mock_conn:
            mock_conn.return_value.__enter__.return_value = mock_db
            mock_db.documents.update_one.return_value.modified_count = 1

            result = Notebook.update_document_notebook(FAKE_DOCUMENT_ID, large_note)
            
            assert result is True
            mock_db.documents.update_one.assert_called_once_with(
                {"_id": ObjectId(FAKE_DOCUMENT_ID)}, 
                {"$set": {"note": large_note}}
            )