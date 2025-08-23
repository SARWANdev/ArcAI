import pytest
from unittest.mock import MagicMock, patch
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from database.repository.project_repository import Project

FAKE_PROJECT_ID = "64b2fae99a8b5c5f12345678"
FAKE_PROJECT = {
    "_id": ObjectId(FAKE_PROJECT_ID),
    "project_name": "Alpha",
    "user_id": "user1",
    "note": "Some notes"
}


@pytest.fixture
def mock_db():
    """Returns a fake DB connection mock."""
    mock_db = MagicMock()
    mock_db.projects = MagicMock()
    return mock_db


def test_save_project_success(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.insert_one.return_value.inserted_id = ObjectId(FAKE_PROJECT_ID)

        project_mock = MagicMock()
        project_mock.new_project_dict.return_value = {"project_name": "Alpha"}

        result = Project.save(project_mock)
        assert result == FAKE_PROJECT_ID


def test_save_project_duplicate_key(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.insert_one.side_effect = DuplicateKeyError("Duplicate")

        project_mock = MagicMock()
        project_mock.new_project_dict.return_value = {"project_name": "Alpha"}

        result = Project.save(project_mock)
        assert result == ""


def test_get_note_success(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find_one.return_value = {"note": "Project notes"}
        result = Project.get_note(FAKE_PROJECT_ID)
        assert result == "Project notes"


def test_get_note_failure_returns_empty_string(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find_one.side_effect = Exception("DB error")
        result = Project.get_note(FAKE_PROJECT_ID)
        assert result == ""


def test_get_project_by_id_success(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find_one.return_value = FAKE_PROJECT
        result = Project.get_project_by_id(FAKE_PROJECT_ID)
        assert result == FAKE_PROJECT


def test_get_project_by_id_raises(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find_one.side_effect = Exception("DB error")
        with pytest.raises(Exception):
            Project.get_project_by_id(FAKE_PROJECT_ID)


def test_get_project_by_name_success(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find_one.return_value = FAKE_PROJECT
        result = Project.get_project_by_name("Alpha")
        assert result == FAKE_PROJECT


def test_get_project_by_name_raises(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find_one.side_effect = Exception("DB error")
        with pytest.raises(Exception):
            Project.get_project_by_name("Alpha")


def test_update_name_success(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn, \
         patch("database.repository.project_repository.get_utc_zulu_timestamp", return_value="timestamp"):
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.update_one.return_value.modified_count = 1
        result = Project.update_name(FAKE_PROJECT_ID, "Beta")
        assert result is True


def test_update_name_failure(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn, \
         patch("database.repository.project_repository.get_utc_zulu_timestamp", return_value="timestamp"):
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.update_one.side_effect = Exception("DB error")
        result = Project.update_name(FAKE_PROJECT_ID, "Beta")
        assert result is False


# -------------------------------
# DELETE PROJECT
# -------------------------------
def test_delete_project_success(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.delete_one.return_value.deleted_count = 1
        result = Project.delete_project(FAKE_PROJECT_ID)
        assert result is True


def test_delete_project_failure(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.delete_one.side_effect = Exception("DB error")
        result = Project.delete_project(FAKE_PROJECT_ID)
        assert result is False


# -------------------------------
# GET USER ID
# -------------------------------
def test_get_user_id_success(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find_one.return_value = {"user_id": "user1"}
        result = Project.get_user_id(FAKE_PROJECT_ID)
        assert result == "user1"


def test_get_user_id_failure(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find_one.side_effect = Exception("DB error")
        result = Project.get_user_id(FAKE_PROJECT_ID)
        assert result == ""


# -------------------------------
# GET PROJECT NAME
# -------------------------------
def test_get_project_name_success(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find_one.return_value = {"project_name": "Alpha"}
        result = Project.get_project_name(FAKE_PROJECT_ID)
        assert result == "Alpha"


def test_get_project_name_failure(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find_one.side_effect = Exception("DB error")
        result = Project.get_project_name(FAKE_PROJECT_ID)
        assert result == ""


# -------------------------------
# PROJECT EXISTS
# -------------------------------
def test_project_exists_true(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find_one.return_value = FAKE_PROJECT
        assert Project.project_exists(FAKE_PROJECT_ID) is True


def test_project_exists_false(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find_one.return_value = None
        assert Project.project_exists(FAKE_PROJECT_ID) is False


def test_project_exists_exception(mock_db):
    with patch("database.repository.project_repository.mongo_connection") as mock_conn:
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_db.projects.find_one.side_effect = Exception("DB error")
        assert Project.project_exists(FAKE_PROJECT_ID) is False
