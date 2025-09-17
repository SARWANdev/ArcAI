import pytest
from unittest.mock import MagicMock, patch
from database.repository.library_repository import Library

FAKE_USER_ID = "user123"
FAKE_PROJECTS = [
    {
        "_id": "project1",
        "project_name": "Alpha",
        "user_id": FAKE_USER_ID,
        "note": "Some notes"
    },
    {
        "_id": "project2", 
        "project_name": "Beta",
        "user_id": FAKE_USER_ID,
        "note": "More notes"
    }
]


@pytest.fixture
def mock_db():
    """Returns a fake DB connection mock."""
    mock_db = MagicMock()
    mock_db.projects = MagicMock()
    return mock_db


def test_get_user_library_success(mock_db):
    """Test successful retrieval of user library."""
    with patch("database.repository.library_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find.return_value = FAKE_PROJECTS

        result = Library.get_user_library(FAKE_USER_ID)
        
        assert result == FAKE_PROJECTS
        mock_db.projects.find.assert_called_once_with({"user_id": FAKE_USER_ID})


def test_get_user_library_empty_result(mock_db):
    """Test retrieval of user library when user has no projects."""
    with patch("database.repository.library_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find.return_value = []

        result = Library.get_user_library(FAKE_USER_ID)
        
        assert result == []
        mock_db.projects.find.assert_called_once_with({"user_id": FAKE_USER_ID})


def test_get_user_library_with_object_id(mock_db):
    """Test retrieval of user library with ObjectId user_id."""
    from bson import ObjectId
    
    object_id_user = ObjectId("64b2fae99a8b5c5f12345678")
    
    with patch("database.repository.library_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find.return_value = FAKE_PROJECTS

        result = Library.get_user_library(object_id_user)
        
        assert result == FAKE_PROJECTS
        mock_db.projects.find.assert_called_once_with({"user_id": object_id_user})


def test_get_user_library_database_exception(mock_db):
    """Test handling of database exceptions during library retrieval."""
    with patch("database.repository.library_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find.side_effect = Exception("Database connection error")

        with pytest.raises(Exception, match="Database connection error"):
            Library.get_user_library(FAKE_USER_ID)


def test_get_user_library_connection_exception(mock_db):
    """Test handling of connection exceptions during library retrieval."""
    with patch("database.repository.library_repository.mongo_connection") as mock_conn:
        mock_conn.side_effect = Exception("Connection failed")

        with pytest.raises(Exception, match="Connection failed"):
            Library.get_user_library(FAKE_USER_ID)


def test_get_user_library_none_user_id(mock_db):
    """Test retrieval of user library with None user_id."""
    with patch("database.repository.library_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find.return_value = []

        result = Library.get_user_library(None)
        
        assert result == []
        mock_db.projects.find.assert_called_once_with({"user_id": None})


def test_get_user_library_empty_string_user_id(mock_db):
    """Test retrieval of user library with empty string user_id."""
    with patch("database.repository.library_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find.return_value = []

        result = Library.get_user_library("")
        
        assert result == []
        mock_db.projects.find.assert_called_once_with({"user_id": ""})


def test_get_user_library_large_result_set(mock_db):
    """Test retrieval of user library with large number of projects."""
    large_project_list = [{"_id": f"project{i}", "project_name": f"Project{i}", "user_id": FAKE_USER_ID} 
                         for i in range(100)]
    
    with patch("database.repository.library_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find.return_value = large_project_list

        result = Library.get_user_library(FAKE_USER_ID)
        
        assert len(result) == 100
        assert result == large_project_list
        mock_db.projects.find.assert_called_once_with({"user_id": FAKE_USER_ID})
