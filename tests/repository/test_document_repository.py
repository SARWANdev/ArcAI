import pytest
from unittest.mock import patch, MagicMock
from bson import ObjectId

from database.repository.document_repository import DocumentRepository


@pytest.fixture
def mock_db():
    """Fixture to provide a fake MongoDB context manager"""
    mock_db = MagicMock()
    return mock_db


def test_save_document(mock_db):
    doc = MagicMock()
    doc.new_document_dict.return_value = {"name": "doc"}
    with patch("database.repository.document_repository.mongo_connection", return_value=MagicMock(__enter__=lambda s: mock_db, __exit__=lambda *a: None)):
        mock_db.documents.insert_one.return_value.inserted_id = ObjectId()
        doc_id = DocumentRepository.save(doc)
        assert isinstance(doc_id, str)
        mock_db.documents.insert_one.assert_called_once()


def test_save_elastic_success():
    with patch("database.repository.document_repository.DocumentRepository.get_name", return_value="doc"), \
         patch("database.repository.document_repository.DocumentRepository.get_authors", return_value="author"), \
         patch("database.repository.document_repository.DocumentRepository.get_user_id", return_value="user"), \
         patch("database.repository.document_repository.es") as mock_es:
        mock_es.index.return_value = True
        result = DocumentRepository.save_elastic("docid", "text")
        assert result is True
        mock_es.index.assert_called_once()


def test_save_elastic_failure():
    with patch("database.repository.document_repository.DocumentRepository.get_name", side_effect=Exception("fail")), \
         patch("database.repository.document_repository.es") as mock_es:
        mock_es.index.side_effect = Exception("fail")
        result = DocumentRepository.save_elastic("docid", "text")
        assert result is False


def test_get_path_success():
    with patch("database.repository.document_repository.DocumentRepository.get_pdf_master_id", return_value="pdfid"), \
         patch("database.repository.document_repository.PdfMasterRepository.get_path", return_value="/tmp/file.pdf"):
        path = DocumentRepository.get_path("docid")
        assert path == "/tmp/file.pdf"


def test_get_metadata_delegations():
    """Covers get_year, get_authors, get_source"""
    with patch("database.repository.document_repository.DocumentRepository.get_pdf_master_id", return_value="pdfid"), \
         patch("database.repository.document_repository.PdfMasterRepository.get_year", return_value="2020"), \
         patch("database.repository.document_repository.PdfMasterRepository.get_authors", return_value="author"), \
         patch("database.repository.document_repository.PdfMasterRepository.get_source", return_value="journal"):
        assert DocumentRepository.get_year("docid") == "2020"
        assert DocumentRepository.get_authors("docid") == "author"
        assert DocumentRepository.get_source("docid") == "journal"


def test_get_name(mock_db):
    with patch("database.repository.document_repository.mongo_connection", return_value=MagicMock(__enter__=lambda s: mock_db, __exit__=lambda *a: None)):
        mock_db.documents.find_one.return_value = {"name": "docname"}
        name = DocumentRepository.get_name("docid")
        assert name == "docname"


def test_set_pdf_master_id(mock_db):
    with patch("database.repository.document_repository.mongo_connection", return_value=MagicMock(__enter__=lambda s: mock_db, __exit__=lambda *a: None)):
        DocumentRepository.set_pdf_master_id("docid", "pdfid")
        mock_db.documents.update_one.assert_called_once()


def test_get_pdf_master_id(mock_db):
    with patch("database.repository.document_repository.mongo_connection", return_value=MagicMock(__enter__=lambda s: mock_db, __exit__=lambda *a: None)):
        mock_db.documents.find_one.return_value = {"pdf_master_id": "pdfid"}
        pdfid = DocumentRepository.get_pdf_master_id("docid")
        assert pdfid == "pdfid"


def test_get_documents_by_project(mock_db):
    with patch("database.repository.document_repository.mongo_connection", return_value=MagicMock(__enter__=lambda s: mock_db, __exit__=lambda *a: None)):
        mock_db.documents.find.return_value = [{"_id": "1"}, {"_id": "2"}]
        docs = DocumentRepository.get_documents_by_project("projid")
        assert isinstance(docs, list)


def test_get_by_document_id(mock_db):
    with patch("database.repository.document_repository.mongo_connection", return_value=MagicMock(__enter__=lambda s: mock_db, __exit__=lambda *a: None)):
        mock_db.documents.find_one.return_value = {"_id": "1", "name": "doc"}
        doc = DocumentRepository.get_by_document_id("docid")
        assert doc["name"] == "doc"


def test_update_document_name_success(mock_db):
    with patch("database.repository.document_repository.mongo_connection", return_value=MagicMock(__enter__=lambda s: mock_db, __exit__=lambda *a: None)), \
         patch("database.repository.document_repository.es") as mock_es, \
         patch("database.repository.document_repository.get_utc_zulu_timestamp", return_value="ts"):
        mock_db.documents.update_one.return_value.modified_count = 1
        result = DocumentRepository.update_document_name("docid", "newname")
        assert result is True
        mock_es.update.assert_called_once()


def test_update_document_name_failure(mock_db):
    with patch("database.repository.document_repository.mongo_connection", side_effect=Exception("fail")):
        result = DocumentRepository.update_document_name("docid", "newname")
        assert result is False


def test_delete_document_success(mock_db):
    with patch("database.repository.document_repository.mongo_connection", return_value=MagicMock(__enter__=lambda s: mock_db, __exit__=lambda *a: None)):
        mock_db.documents.delete_one.return_value.deleted_count = 1
        result = DocumentRepository.delete_document("docid")
        assert result is True


def test_delete_document_failure(mock_db):
    with patch("database.repository.document_repository.mongo_connection", side_effect=Exception("fail")):
        result = DocumentRepository.delete_document("docid")
        assert result is False


def test_delete_elastic_success():
    with patch("database.repository.document_repository.es") as mock_es:
        result = DocumentRepository.delete_elastic("docid")
        assert result is True
        mock_es.delete.assert_called_once()


def test_delete_elastic_failure():
    with patch("database.repository.document_repository.es") as mock_es:
        mock_es.delete.side_effect = Exception("fail")
        result = DocumentRepository.delete_elastic("docid")
        assert result is False


def test_get_note_success(mock_db):
    with patch("database.repository.document_repository.mongo_connection", return_value=MagicMock(__enter__=lambda s: mock_db, __exit__=lambda *a: None)):
        mock_db.documents.find_one.return_value = {"note": "note text"}
        note = DocumentRepository.get_note("docid")
        assert note == "note text"


def test_get_bibtex_success():
    with patch("database.repository.document_repository.DocumentRepository.get_pdf_master_id", return_value="pdfid"), \
         patch("database.repository.document_repository.PdfMasterRepository.get_bibtex", return_value="@bib{...}"):
        bib = DocumentRepository.get_bibtex_by_document_id("docid")
        assert "@bib" in bib


def test_get_bibtex_failure():
    with patch("database.repository.document_repository.DocumentRepository.get_pdf_master_id", side_effect=Exception("fail")):
        bib = DocumentRepository.get_bibtex_by_document_id("docid")
        assert bib == ""


def test_search_documents_success():
    with patch("database.repository.document_repository.es") as mock_es:
        mock_es.search.return_value = {"hits": {"hits": [{"_id": "1", "_source": {"name": "doc", "author": "a"}}]}}
        docs = DocumentRepository.search_documents("user", "query")
        assert docs[0]["id"] == "1"


def test_search_contents_success():
    with patch("database.repository.document_repository.es") as mock_es:
        mock_es.search.return_value = {"hits": {"hits": [{"_id": "1", "_source": {"name": "doc", "author": "a", "text": "t"}}]}}
        docs = DocumentRepository.search_contents("user", "query")
        assert docs[0]["text"] == "t"


def test_get_user_id_success():
    with patch("database.repository.document_repository.DocumentRepository.get_pdf_master_id", return_value="pdfid"), \
         patch("database.repository.document_repository.PdfMasterRepository.get_user_id", return_value="user"):
        uid = DocumentRepository.get_user_id("docid")
        assert uid == "user"


def test_user_exists_true(mock_db):
    with patch("database.repository.document_repository.mongo_connection", return_value=MagicMock(__enter__=lambda s: mock_db, __exit__=lambda *a: None)):
        mock_db.users.find_one.return_value = {"_id": "user1"}
        exists = DocumentRepository.user_exists("user1")
        assert exists is True


def test_user_exists_false(mock_db):
    with patch("database.repository.document_repository.mongo_connection", side_effect=Exception("fail")):
        exists = DocumentRepository.user_exists("user1")
        assert exists is False
