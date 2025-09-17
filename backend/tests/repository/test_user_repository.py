import pytest
import mongomock
from unittest.mock import patch, MagicMock
from types import SimpleNamespace
from database.repository.user_repository import UserRepository
from model.user_profile.user import User


@pytest.fixture
def mock_mongo():
    """Fixture to patch mongo_connection with mongomock as a context manager"""
    db = mongomock.MongoClient().db
    context_manager = MagicMock()
    context_manager.__enter__.return_value = db
    context_manager.__exit__.return_value = None
    with patch("database.repository.user_repository.mongo_connection", return_value=context_manager) as mock_conn:
        yield db


@pytest.fixture
def sample_user():
    """Fixture for a sample User object"""
    user = MagicMock(spec=User)
    user_dict = {
        "_id": "user123",
        "username": "test_user",
        "active": True,
        "view_mode": False
    }
    user.new_user_dict.return_value = user_dict
    return user


def test_save_new_user(mock_mongo, sample_user):
    user_id = UserRepository.save(sample_user)
    assert user_id == "user123"
    saved_user = mock_mongo.users.find_one({"_id": "user123"})
    assert saved_user["username"] == "test_user"


def test_save_duplicate_user(mock_mongo, sample_user):
    mock_mongo.users.insert_one(sample_user.new_user_dict())  # Insert once
    # Simulate DuplicateKeyError
    with patch("pymongo.collection.Collection.insert_one", side_effect=Exception("DuplicateKeyError")):
        result = UserRepository.save(sample_user)
        assert result == ""


def test_get_user_by_id(mock_mongo, sample_user):
    mock_mongo.users.insert_one(sample_user.new_user_dict())
    user = UserRepository.get_user_by_id("user123")
    assert user["_id"] == "user123"
    assert user["username"] == "test_user"


def test_update_view_mode(mock_mongo, sample_user):
    mock_mongo.users.insert_one(sample_user.new_user_dict())
    # Patch update_one to return modified_count=1
    with patch("pymongo.collection.Collection.update_one", return_value=SimpleNamespace(modified_count=1)):
        updated = UserRepository.update_view_mode("user123", True)
        assert updated is True
    user = mock_mongo.users.find_one({"_id": "user123"})
    assert user["view_mode"] is True


def test_deactivate_user(mock_mongo, sample_user):
    mock_mongo.users.insert_one(sample_user.new_user_dict())
    with patch("pymongo.collection.Collection.update_one", return_value=SimpleNamespace(modified_count=1)):
        result = UserRepository.deactivate_user("user123")
        assert result is True
    user = mock_mongo.users.find_one({"_id": "user123"})
    assert user["active"] is False


def test_activate_user(mock_mongo, sample_user):
    user_data = sample_user.new_user_dict()
    user_data["active"] = False
    mock_mongo.users.insert_one(user_data)
    with patch("pymongo.collection.Collection.update_one", return_value=SimpleNamespace(modified_count=1)):
        result = UserRepository.activate_user("user123")
        assert result is True
    user = mock_mongo.users.find_one({"_id": "user123"})
    assert user["active"] is True


def test_get_view_mode(mock_mongo, sample_user):
    mock_mongo.users.insert_one(sample_user.new_user_dict())
    mode = UserRepository.get_view_mode("user123")
    assert mode is False
    with patch("pymongo.collection.Collection.update_one", return_value=SimpleNamespace(modified_count=1)):
        UserRepository.update_view_mode("user123", True)
    mode = UserRepository.get_view_mode("user123")
    assert mode is True


def test_user_exists(mock_mongo, sample_user):
    mock_mongo.users.insert_one(sample_user.new_user_dict())
    exists = UserRepository.user_exists("user123")
    assert exists is True
    exists = UserRepository.user_exists("not_real")
    assert exists is False
