from database.repository.date_time_utils import get_utc_zulu_timestamp
from services.upload_manager.document_upload_service import get_pdf_sha256


class PdfMaster:
    def __init__(self, path: str, pdf_hash, user_id):
        self.path = path
        self.hash = pdf_hash
        self.user_id = user_id

    def to_dict(self) -> dict:
        pdf_master_data = {
            "user_id": self.user_id,
            "path": self.path,
            "ref_count": 0,
            "hash": self.hash,
            "vector_store_path": "",
            "journal": "",
            "first_author": "",
            "year": None,
            "pages": None,
            "bibtex": None,

            "created_at": get_utc_zulu_timestamp(),
            "updated_at": get_utc_zulu_timestamp(),
        }
        return pdf_master_data