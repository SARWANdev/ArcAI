import pytest
import mongomock
from unittest.mock import patch, MagicMock
from bson import ObjectId
from services.bibtex_service import BibTeX_Service
from database.repository.pdf_master_repository import PdfMasterRepository
from model.document_reader.pdf_master import PdfMaster
from database.repository.date_time_utils import get_utc_zulu_timestamp


@pytest.fixture
def mock_mongo():
    """Patch mongo_connection to return a mongomock database"""
    with patch("database.repository.pdf_master_repository.mongo_connection", return_value=mongomock.MongoClient().db) as mock_conn:
        yield mock_conn


@pytest.fixture
def sample_pdf():
    """Return a sample PdfMaster object"""
    pdf = MagicMock(spec=PdfMaster)
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
    db = mock_mongo.return_value
    saved = db.pdf_master.find_one({"_id": ObjectId(pdf_id)})
    assert saved["hash"] == pdf_dict["hash"]


def test_delete_pdf_master_success(mock_mongo, sample_pdf):
    pdf, pdf_dict = sample_pdf
    db = mock_mongo.return_value
    inserted_id = db.pdf_master.insert_one(pdf_dict).inserted_id
    result = PdfMasterRepository.delete_pdf_master(str(inserted_id))
    assert result is True
    assert db.pdf_master.count_documents({"_id": inserted_id}) == 0


def test_delete_pdf_master_not_found(mock_mongo):
    result = PdfMasterRepository.delete_pdf_master(str(ObjectId()))
    assert result is False


def test_increment_and_decrement_ref_count(mock_mongo, sample_pdf):
    pdf, pdf_dict = sample_pdf
    db = mock_mongo.return_value
    inserted_id = db.pdf_master.insert_one(pdf_dict).inserted_id

    PdfMasterRepository.increment_ref_count(str(inserted_id))
    ref_count = db.pdf_master.find_one({"_id": inserted_id})["ref_count"]
    assert ref_count == 1

    PdfMasterRepository.decrement_ref_count(str(inserted_id))
    ref_count = db.pdf_master.find_one({"_id": inserted_id})["ref_count"]
    assert ref_count == 0


def test_get_ref_count(mock_mongo, sample_pdf):
    pdf, pdf_dict = sample_pdf
    db = mock_mongo.return_value
    inserted_id = db.pdf_master.insert_one(pdf_dict).inserted_id
    count = PdfMasterRepository.get_ref_count(str(inserted_id))
    assert count == 0


def test_get_and_set_path(mock_mongo, sample_pdf):
    pdf, pdf_dict = sample_pdf
    db = mock_mongo.return_value
    inserted_id = db.pdf_master.insert_one(pdf_dict).inserted_id

    path = PdfMasterRepository.get_path(str(inserted_id))
    assert path == pdf_dict["path"]

    PdfMasterRepository.set_path(str(inserted_id), "/new/path.pdf")
    updated_path = db.pdf_master.find_one({"_id": inserted_id})["path"]
    assert updated_path == "/new/path.pdf"


def test_get_and_set_vector_path(mock_mongo, sample_pdf):
    pdf, pdf_dict = sample_pdf
    db = mock_mongo.return_value
    inserted_id = db.pdf_master.insert_one(pdf_dict).inserted_id

    path = PdfMasterRepository.get_vector_path(str(inserted_id))
    assert path == pdf_dict["vector_store_path"]

    PdfMasterRepository.set_vector_path(str(inserted_id), "/new/vector")
    updated = db.pdf_master.find_one({"_id": inserted_id})["vector_store_path"]
    assert updated == "/new/vector"


def test_get_and_set_journal(mock_mongo, sample_pdf):
    pdf, pdf_dict = sample_pdf
    db = mock_mongo.return_value
    inserted_id = db.pdf_master.insert_one(pdf_dict).inserted_id

    journal = PdfMasterRepository.get_journal(str(inserted_id))
    assert journal == pdf_dict["journal"]

    PdfMasterRepository.set_journal(str(inserted_id), "New Journal")
    updated = db.pdf_master.find_one({"_id": inserted_id})["journal"]
    assert updated == "New Journal"


def test_get_and_set_first_author(mock_mongo, sample_pdf):
    pdf, pdf_dict = sample_pdf
    db = mock_mongo.return_value
    inserted_id = db.pdf_master.insert_one(pdf_dict).inserted_id

    author = PdfMasterRepository.get_first_author(str(inserted_id))
    assert author == pdf_dict["first_author"]

    PdfMasterRepository.set_first_author(str(inserted_id), "Alice")
    updated = db.pdf_master.find_one({"_id": inserted_id})["first_author"]
    assert updated == "Alice"


def test_set_bibtex(mock_mongo, sample_pdf):
    pdf, pdf_dict = sample_pdf
    db = mock_mongo.return_value
    inserted_id = db.pdf_master.insert_one(pdf_dict).inserted_id

    bibtex_mock = MagicMock()
    bibtex_mock.get_first_author.return_value = "Alice"
    bibtex_mock.get_year.return_value = "2025"
    bibtex_mock.get_authors.return_value = "Alice, Bob"
    bibtex_mock.get_source.return_value = "arxiv"
    bibtex_mock.get_title.return_value = "Title"

    with patch.object(BibTeX_Service, "from_bibtex", return_value=bibtex_mock):
        PdfMasterRepository.set_bibtex(str(inserted_id), "@article{test}")

    doc = db.pdf_master.find_one({"_id": inserted_id})
    assert doc["bibtex"] == "@article{test}"
    assert doc["first_author"] == "Alice"
    assert doc["year"] == "2025"
    assert doc["authors"] == "Alice, Bob"
    assert doc["source"] == "arxiv"
    assert doc["title"] == "Title"


def test_is_document_uploaded(mock_mongo, sample_pdf):
    pdf, pdf_dict = sample_pdf
    db = mock_mongo.return_value
    db.pdf_master.insert_one(pdf_dict)

    uploaded = PdfMasterRepository.is_document_uploaded("hash123", "user123")
    assert uploaded is not None

    uploaded_none = PdfMasterRepository.is_document_uploaded("nohash", "user123")
    assert uploaded_none is None
