from database.repository.date_time_utils import get_utc_zulu_timestamp
from services.upload_manager.document_upload_service import get_pdf_sha256


class PdfMaster:
    def __init__(self, path: str, pdf_hash, user_id, vector_store_path = None, journal = None, authors = None,
                 first_author = None, year = None, source = None, bibtex = None):
        self.path = path
        self.hash = pdf_hash
        self.user_id = user_id
        self.vector_store_path = vector_store_path
        self.journal = journal
        self.authors = authors
        self.first_author = first_author
        self.year = year
        self.source = source
        self.bibtex = bibtex

    def new_pdf_master_dict(self) -> dict:
        pdf_master_data = {
            "user_id": self.user_id,
            "path": self.path,
            "ref_count": 0,
            "hash": self.hash,
            "vector_store_path": "",
            "journal": "",
            "authors": "",
            "first_author": "",
            "year": "",
            "pages": "",
            "source": "",
            "bibtex": "",

            "created_at": get_utc_zulu_timestamp(),
            "updated_at": get_utc_zulu_timestamp(),
        }
        return pdf_master_data