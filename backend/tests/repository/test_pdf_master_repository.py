import pytest
import mongomock
from unittest.mock import patch, MagicMock
from bson import ObjectId
from services.bibtex_service import BibTeX_Service
from database.repository.pdf_master_repository import PdfMasterRepository

@pytest.fixture
def mock_mongo():
    # Make mongo_connection() behave like a context manager
    with patch("database.repository.pdf_master_repository.mongo_connection") as mock_conn:
        mock_db = mongomock.MongoClient().db
        mock_conn.return_value.__enter__.return_value = mock_db
        mock_conn.return_value.__exit__.return_value = False
        yield mock_db 

@pytest.fixture
def sample_pdf():
    pdf = MagicMock()
    pdf_dict = {
        "_id": ObjectId(),
        "hash": "hash123",
        "user_id": "user123",
        "ref_count": 0,
        "path": "/tmp/file.pdf",
        "vector_store_path": "/tmp/vector",
        "first_author": "John Doe",
        "year": "2025",
        "pages": 10,
        "journal": "Test Journal",
        "authors": "John Doe, Jane Smith",
        "source": "arxiv",
        "bibtex": "@article{test}"
    }
    pdf.new_pdf_master_dict.return_value = pdf_dict
    return pdf, pdf_dict

def test_save_pdf_master(mock_mongo, sample_pdf):
    pdf, pdf_dict = sample_pdf
    pdf_id = PdfMasterRepository.save(pdf)
    saved = mock_mongo.pdf_master.find_one({"_id": ObjectId(pdf_id)})
    assert saved["hash"] == pdf_dict["hash"]

def test_delete_pdf_master_success(mock_mongo, sample_pdf):
    _, pdf_dict = sample_pdf
    inserted_id = mock_mongo.pdf_master.insert_one(pdf_dict).inserted_id
    result = PdfMasterRepository.delete_pdf_master(str(inserted_id))
    assert result is True
    assert mock_mongo.pdf_master.count_documents({"_id": inserted_id}) == 0

def test_delete_pdf_master_not_found(mock_mongo):
    result = PdfMasterRepository.delete_pdf_master(str(ObjectId()))
    assert result is False

def test_increment_and_decrement_ref_count(mock_mongo, sample_pdf):
    _, pdf_dict = sample_pdf
    inserted_id = mock_mongo.pdf_master.insert_one(pdf_dict).inserted_id

    PdfMasterRepository.increment_ref_count(str(inserted_id))
    assert mock_mongo.pdf_master.find_one({"_id": inserted_id})["ref_count"] == 1

    PdfMasterRepository.decrement_ref_count(str(inserted_id))
    assert mock_mongo.pdf_master.find_one({"_id": inserted_id})["ref_count"] == 0

def test_get_ref_count(mock_mongo, sample_pdf):
    _, pdf_dict = sample_pdf
    inserted_id = mock_mongo.pdf_master.insert_one(pdf_dict).inserted_id
    assert PdfMasterRepository.get_ref_count(str(inserted_id)) == 0

def test_get_and_set_path(mock_mongo, sample_pdf):
    _, pdf_dict = sample_pdf
    inserted_id = mock_mongo.pdf_master.insert_one(pdf_dict).inserted_id

    assert PdfMasterRepository.get_path(str(inserted_id)) == pdf_dict["path"]
    PdfMasterRepository.set_path(str(inserted_id), "/new/path.pdf")
    assert mock_mongo.pdf_master.find_one({"_id": inserted_id})["path"] == "/new/path.pdf"

def test_get_and_set_vector_path(mock_mongo, sample_pdf):
    _, pdf_dict = sample_pdf
    inserted_id = mock_mongo.pdf_master.insert_one(pdf_dict).inserted_id

    assert PdfMasterRepository.get_vector_path(str(inserted_id)) == pdf_dict["vector_store_path"]
    PdfMasterRepository.set_vector_path(str(inserted_id), "/new/vector")
    assert mock_mongo.pdf_master.find_one({"_id": inserted_id})["vector_store_path"] == "/new/vector"

def test_get_and_set_journal(mock_mongo, sample_pdf):
    _, pdf_dict = sample_pdf
    inserted_id = mock_mongo.pdf_master.insert_one(pdf_dict).inserted_id

    assert PdfMasterRepository.get_journal(str(inserted_id)) == pdf_dict["journal"]
    PdfMasterRepository.set_journal(str(inserted_id), "New Journal")
    assert mock_mongo.pdf_master.find_one({"_id": inserted_id})["journal"] == "New Journal"

def test_get_and_set_first_author(mock_mongo, sample_pdf):
    _, pdf_dict = sample_pdf
    inserted_id = mock_mongo.pdf_master.insert_one(pdf_dict).inserted_id

    assert PdfMasterRepository.get_first_author(str(inserted_id)) == pdf_dict["first_author"]
    PdfMasterRepository.set_first_author(str(inserted_id), "Alice")
    assert mock_mongo.pdf_master.find_one({"_id": inserted_id})["first_author"] == "Alice"

def test_set_bibtex_updates_metadata(mock_mongo, sample_pdf):
    _, pdf_dict = sample_pdf
    inserted_id = mock_mongo.pdf_master.insert_one(pdf_dict).inserted_id

    bibtex_mock = MagicMock()
    bibtex_mock.get_first_author.return_value = "Alice"
    bibtex_mock.get_year.return_value = "2025"
    bibtex_mock.get_authors.return_value = "Alice, Bob"
    bibtex_mock.get_source.return_value = "arxiv"
    bibtex_mock.get_title.return_value = "Title"

    with patch.object(BibTeX_Service, "from_bibtex", return_value=bibtex_mock):
        PdfMasterRepository.set_bibtex(str(inserted_id), "@article{test}")

    doc = mock_mongo.pdf_master.find_one({"_id": inserted_id})
    assert doc["bibtex"] == "@article{test}"
    assert doc["first_author"] == "Alice"
    assert doc["year"] == "2025"
    assert doc["authors"] == "Alice, Bob"
    assert doc["source"] == "arxiv"
    assert doc["title"] == "Title"
    assert "updated_at" in doc

def test_is_document_uploaded(mock_mongo, sample_pdf):
    _, pdf_dict = sample_pdf
    mock_mongo.pdf_master.insert_one(pdf_dict)

    assert PdfMasterRepository.is_document_uploaded("hash123", "user123") is not None
    assert PdfMasterRepository.is_document_uploaded("nohash", "user123") is None

def test_get_pdf_hash(mock_mongo, sample_pdf):
    _, pdf_dict = sample_pdf
    inserted_id = mock_mongo.pdf_master.insert_one(pdf_dict).inserted_id
    assert PdfMasterRepository.get_pdf_hash(str(inserted_id)) == "hash123"

def test_remote_paths_and_user_id(mock_mongo, sample_pdf):
    _, pdf_dict = sample_pdf
    inserted_id = mock_mongo.pdf_master.insert_one(pdf_dict).inserted_id

    # remote faiss
    PdfMasterRepository.set_remote_faiss_path(str(inserted_id), "/faiss/remote")
    assert PdfMasterRepository.get_remote_faiss_path(str(inserted_id)) == "/faiss/remote"

    # remote pkl
    PdfMasterRepository.set_remote_pkl_path(str(inserted_id), "/pkl/remote")
    assert PdfMasterRepository.get_remote_pkl_path(str(inserted_id)) == "/pkl/remote"

    # user_id
    assert PdfMasterRepository.get_user_id(str(inserted_id)) == "user123"

@pytest.fixture
def mock_mongo_ctx_ok():
    with patch("database.repository.pdf_master_repository.mongo_connection") as mock_conn:
        db = mongomock.MongoClient().db
        mock_conn.return_value.__enter__.return_value = db
        mock_conn.return_value.__exit__.return_value = False
        yield db

@pytest.fixture
def mock_mongo_ctx_err():
    with patch("database.repository.pdf_master_repository.mongo_connection") as mock_conn:
        db = MagicMock()
        db.pdf_master.find_one.side_effect = Exception("boom find_one")
        db.pdf_master.update_one.side_effect = Exception("boom update_one")
        db.pdf_master.delete_one.side_effect = Exception("boom delete_one")
        mock_conn.return_value.__enter__.return_value = db
        mock_conn.return_value.__exit__.return_value = False
        yield db

def test_get_pdf_hash_success(mock_mongo_ctx_ok):
    doc_id = mock_mongo_ctx_ok.pdf_master.insert_one({"hash": "h123"}).inserted_id
    assert PdfMasterRepository.get_pdf_hash(str(doc_id)) == "h123"

def test_year_set_get_success(mock_mongo_ctx_ok):
    doc_id = mock_mongo_ctx_ok.pdf_master.insert_one({"year": "1999"}).inserted_id
    assert PdfMasterRepository.get_year(str(doc_id)) == "1999"
    PdfMasterRepository.set_year(str(doc_id), "2025")
    assert mock_mongo_ctx_ok.pdf_master.find_one({"_id": doc_id})["year"] == "2025"

def test_pages_set_get_success(mock_mongo_ctx_ok):
    doc_id = mock_mongo_ctx_ok.pdf_master.insert_one({"pages": 7}).inserted_id
    assert PdfMasterRepository.get_pages(str(doc_id)) == 7
    PdfMasterRepository.set_pages(str(doc_id), 10)
    assert mock_mongo_ctx_ok.pdf_master.find_one({"_id": doc_id})["pages"] == 10

def test_authors_set_get_success(mock_mongo_ctx_ok):
    doc_id = mock_mongo_ctx_ok.pdf_master.insert_one({"authors": "A, B"}).inserted_id
    assert PdfMasterRepository.get_authors(str(doc_id)) == "A, B"
    PdfMasterRepository.set_authors(str(doc_id), "C, D")
    assert mock_mongo_ctx_ok.pdf_master.find_one({"_id": doc_id})["authors"] == "C, D"

def test_source_set_get_success(mock_mongo_ctx_ok):
    doc_id = mock_mongo_ctx_ok.pdf_master.insert_one({"source": "arxiv"}).inserted_id
    assert PdfMasterRepository.get_source(str(doc_id)) == "arxiv"
    PdfMasterRepository.set_source(str(doc_id), "ieee")
    assert mock_mongo_ctx_ok.pdf_master.find_one({"_id": doc_id})["source"] == "ieee"

def test_remote_paths_set_get_success(mock_mongo_ctx_ok):
    doc_id = mock_mongo_ctx_ok.pdf_master.insert_one({}).inserted_id
    PdfMasterRepository.set_remote_faiss_path(str(doc_id), "/faiss/remote")
    assert PdfMasterRepository.get_remote_faiss_path(str(doc_id)) == "/faiss/remote"
    PdfMasterRepository.set_remote_pkl_path(str(doc_id), "/pkl/remote")
    assert PdfMasterRepository.get_remote_pkl_path(str(doc_id)) == "/pkl/remote"

def test_get_user_id_success(mock_mongo_ctx_ok):
    doc_id = mock_mongo_ctx_ok.pdf_master.insert_one({"user_id": "u1"}).inserted_id
    assert PdfMasterRepository.get_user_id(str(doc_id)) == "u1"

def test_get_bibtex_success(mock_mongo_ctx_ok):
    doc_id = mock_mongo_ctx_ok.pdf_master.insert_one({"bibtex": "@x"}).inserted_id
    assert PdfMasterRepository.get_bibtex(str(doc_id)) == "@x"

def test_get_pdf_hash_error_default(mock_mongo_ctx_err):
    assert PdfMasterRepository.get_pdf_hash(str(ObjectId())) == ""

def test_get_path_error_default(mock_mongo_ctx_err):
    assert PdfMasterRepository.get_path(str(ObjectId())) == ""

def test_get_vector_path_error_default(mock_mongo_ctx_err):
    assert PdfMasterRepository.get_vector_path(str(ObjectId())) == ""

def test_get_journal_error_default(mock_mongo_ctx_err):
    assert PdfMasterRepository.get_journal(str(ObjectId())) == ""

def test_get_first_author_error_default(mock_mongo_ctx_err):
    assert PdfMasterRepository.get_first_author(str(ObjectId())) == ""

def test_get_year_error_default(mock_mongo_ctx_err):
    assert PdfMasterRepository.get_year(str(ObjectId())) == ""

def test_get_pages_error_default(mock_mongo_ctx_err):
    assert PdfMasterRepository.get_pages(str(ObjectId())) == ""

def test_get_bibtex_error_default(mock_mongo_ctx_err):
    assert PdfMasterRepository.get_bibtex(str(ObjectId())) == ""

def test_get_authors_error_default(mock_mongo_ctx_err):
    assert PdfMasterRepository.get_authors(str(ObjectId())) == ""

def test_get_source_error_default(mock_mongo_ctx_err):
    assert PdfMasterRepository.get_source(str(ObjectId())) == ""

def test_get_remote_faiss_path_error_default(mock_mongo_ctx_err):
    assert PdfMasterRepository.get_remote_faiss_path(str(ObjectId())) is None

def test_get_remote_pkl_path_error_default(mock_mongo_ctx_err):
    assert PdfMasterRepository.get_remote_pkl_path(str(ObjectId())) is None

def test_get_user_id_error_default(mock_mongo_ctx_err):
    assert PdfMasterRepository.get_user_id(str(ObjectId())) is None

def test_get_ref_count_error_default(mock_mongo_ctx_err):
    assert PdfMasterRepository.get_ref_count(str(ObjectId())) is None

def test_set_path_error_no_raise(mock_mongo_ctx_err):
    PdfMasterRepository.set_path(str(ObjectId()), "/x")

def test_set_vector_path_error_no_raise(mock_mongo_ctx_err):
    PdfMasterRepository.set_vector_path(str(ObjectId()), "/v")

def test_set_journal_error_no_raise(mock_mongo_ctx_err):
    PdfMasterRepository.set_journal(str(ObjectId()), "J")

def test_set_first_author_error_no_raise(mock_mongo_ctx_err):
    PdfMasterRepository.set_first_author(str(ObjectId()), "A")

def test_set_year_error_no_raise(mock_mongo_ctx_err):
    PdfMasterRepository.set_year(str(ObjectId()), "2000")

def test_set_pages_error_no_raise(mock_mongo_ctx_err):
    PdfMasterRepository.set_pages(str(ObjectId()), 9)

def test_set_authors_error_no_raise(mock_mongo_ctx_err):
    PdfMasterRepository.set_authors(str(ObjectId()), "A, B")

def test_set_source_error_no_raise(mock_mongo_ctx_err):
    PdfMasterRepository.set_source(str(ObjectId()), "s")

def test_set_remote_faiss_path_error_no_raise(mock_mongo_ctx_err):
    PdfMasterRepository.set_remote_faiss_path(str(ObjectId()), "/faiss")

def test_set_remote_pkl_path_error_no_raise(mock_mongo_ctx_err):
    PdfMasterRepository.set_remote_pkl_path(str(ObjectId()), "/pkl")

def test_increment_ref_count_error_no_raise(mock_mongo_ctx_err):
    PdfMasterRepository.increment_ref_count(str(ObjectId()))

def test_decrement_ref_count_error_no_raise(mock_mongo_ctx_err):
    PdfMasterRepository.decrement_ref_count(str(ObjectId()))

def test_delete_pdf_master_exception_returns_false(mock_mongo_ctx_err):
    assert PdfMasterRepository.delete_pdf_master(str(ObjectId())) is False
