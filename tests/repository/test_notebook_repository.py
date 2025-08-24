import pytest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from database.repository.notebook_repository import Notebook

def test_get_project_notebook_success():
    mock_db = MagicMock()
    project_id = ObjectId()
    mock_db.projects.find_one.return_value = {"_id": project_id, "note": "Initial project note"}
    with patch("database.utils.mongo_connector.mongo_connection", return_value=mock_db):
        note = Notebook.get_project_notebook(str(project_id))
        assert note == "Initial project note"

def test_get_project_notebook_not_found():
    mock_db = MagicMock()
    mock_db.projects.find_one.return_value = None
    with patch("database.utils.mongo_connector.mongo_connection", return_value=mock_db):
        note = Notebook.get_project_notebook(str(ObjectId()))
        assert note == ""

def test_get_project_notebook_no_note_field():
    mock_db = MagicMock()
    project_id = ObjectId()
    mock_db.projects.find_one.return_value = {"_id": project_id}
    with patch("database.utils.mongo_connector.mongo_connection", return_value=mock_db):
        note = Notebook.get_project_notebook(str(project_id))
        assert note == ""

def test_update_project_notebook_success():
    mock_db = MagicMock()
    project_id = ObjectId()
    mock_result = MagicMock()
    mock_result.modified_count = 1
    mock_db.projects.update_one.return_value = mock_result
    with patch("database.utils.mongo_connector.mongo_connection", return_value=mock_db):
        result = Notebook.update_project_notebook(str(project_id), "Updated project note.")
        assert result is True

def test_update_project_notebook_not_found():
    mock_db = MagicMock()
    mock_result = MagicMock()
    mock_result.modified_count = 0
    mock_db.projects.update_one.return_value = mock_result
    with patch("database.utils.mongo_connector.mongo_connection", return_value=mock_db):
        result = Notebook.update_project_notebook(str(ObjectId()), "Some note")
        assert result is False

def test_get_document_notebook_success():
    mock_db = MagicMock()
    document_id = ObjectId()
    mock_db.documents.find_one.return_value = {"_id": document_id, "note": "Initial document note"}
    with patch("database.utils.mongo_connector.mongo_connection", return_value=mock_db):
        note = Notebook.get_document_notebook(str(document_id))
        assert note == "Initial document note"

def test_get_document_notebook_not_found():
    mock_db = MagicMock()
    mock_db.documents.find_one.return_value = None
    with patch("database.utils.mongo_connector.mongo_connection", return_value=mock_db):
        note = Notebook.get_document_notebook(str(ObjectId()))
        assert note == ""

def test_get_document_notebook_no_note_field():
    mock_db = MagicMock()
    document_id = ObjectId()
    mock_db.documents.find_one.return_value = {"_id": document_id}
    with patch("database.utils.mongo_connector.mongo_connection", return_value=mock_db):
        note = Notebook.get_document_notebook(str(document_id))
        assert note == ""

def test_update_document_notebook_success():
    mock_db = MagicMock()
    document_id = ObjectId()
    mock_result = MagicMock()
    mock_result.modified_count = 1
    mock_db.documents.update_one.return_value = mock_result
    with patch("database.utils.mongo_connector.mongo_connection", return_value=mock_db):
        result = Notebook.update_document_notebook(str(document_id), "Updated document note.")
        assert result is True

def test_update_document_notebook_not_found():
    mock_db = MagicMock()
    mock_result = MagicMock()
    mock_result.modified_count = 0
    mock_db.documents.update_one.return_value = mock_result
    with patch("database.utils.mongo_connector.mongo_connection", return_value=mock_db):
        result = Notebook.update_document_notebook(str(ObjectId()), "Some note")
        assert result is False