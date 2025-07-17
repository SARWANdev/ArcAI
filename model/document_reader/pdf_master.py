from database.repository.date_time_utils import get_utc_zulu_timestamp
from services.upload_manager.hash_manager import get_pdf_sha256


class PdfMaster:
    def __init__(self, path: str, pdf_hash, user_id, vector_store_path = None, journal = None, authors = None,
                 first_author = None, year = None, source = None, bibtex = None):
        self.path = path
        self.hash = pdf_hash
        self.user_id = user_id
        self.vector_store_path = vector_store_path or ""
        self.journal = journal or ""
        self.authors = authors or ""
        self.first_author = first_author or ""
        self.year = year or ""
        self.source = source or ""
        self.bibtex = bibtex or ""

    def new_pdf_master_dict(self) -> dict:
        pdf_master_data = {
            "user_id": self.user_id,
            "path": self.path,
            "ref_count": 0,
            "hash": self.hash,
            "vector_store_path": self.vector_store_path,
            "journal": self.journal,
            "authors": self.authors,
            "first_author": self.first_author,
            "year": self.year,
            "source": self.source,
            "bibtex": self.bibtex,

            "created_at": get_utc_zulu_timestamp(),
            "updated_at": get_utc_zulu_timestamp(),
        }
        return pdf_master_data