import pytest
from pymongo import MongoClient


@pytest.fixture(scope="function")
def db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ArcAI"]

    # Clean collections before every test
    for name in db.list_collection_names():
        db[name].delete_many({})

    yield db

    # Cleaning after every test
    for name in db.list_collection_names():
        db[name].delete_many({})
    client.close()


def test_collections_exist(db):
    db.users.insert_one({"email": "temp"})  # fuerza creación
    db.projects.insert_one({"user_id": 1})
    db.documents.insert_one({"project_id": 1})
    db.conversations.insert_one({"user_id": 1})

    expected = {"users", "projects", "documents", "conversations"}
    actual = set(db.list_collection_names())
    for coll in expected:
        assert coll in actual, f"{coll} no existe en la base de datos"


def test_indexes_users(db):
    db.users.create_index("email", unique=True)
    indexes = db.users.index_information()
    assert "email_1" in indexes
    assert indexes["email_1"].get("unique", False)


def test_indexes_documents(db):
    db.documents.create_index("project_id")
    db.documents.create_index("favorite")
    db.documents.create_index("read")

    indexes = db.documents.index_information()
    for field in ["project_id_1", "favorite_1", "read_1"]:
        assert field in indexes


def test_insert_and_find_user(db):
    db.users.create_index("email", unique=True)
    db.users.insert_one({"email": "test@example.com", "name": "Test"})
    user = db.users.find_one({"email": "test@example.com"})
    assert user is not None
    assert user["name"] == "Test"
