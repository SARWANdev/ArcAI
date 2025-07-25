from database.repository.date_time_utils import get_utc_zulu_timestamp


class PdfMaster:
    def __init__(self, path: str, pdf_hash, user_id, remote_pkl_path = None, remote_faiss_path = None, journal = None, authors = None,
                 first_author = None, year = None, source = None, bibtex = None):
        """
        Initializes a PdfMaster instance with the given details.
        
        :param path: The file path of the PDF.
        :type path: str
        :param pdf_hash: The hash of the PDF for deduplication.
        :type pdf_hash: str
        :param user_id: The user ID who owns the PDF.
        :type user_id: str
        :param remote_pkl_path: The remote path for the pkl file (optional).
        :type remote_pkl_path: str | None
        :param remote_faiss_path: The remote path for the FAISS index (optional).
        :type remote_faiss_path: str | None
        :param journal: The journal the paper is from (optional).
        :type journal: str | None
        :param authors: Authors of the paper (optional).
        :type authors: str | None
        :param first_author: The first author of the paper (optional).
        :type first_author: str | None
        :param year: The year of publication (optional).
        :type year: str | None
        :param source: The source of the paper (optional).
        :type source: str | None
        :param bibtex: The BibTeX entry for the paper (optional).
        :type bibtex: str | None
        """
        self.path = path
        self.hash = pdf_hash
        self.user_id = user_id
        self.remote_faiss_path = remote_faiss_path or ""
        self.remote_pkl_path = remote_pkl_path or ""
        self.journal = journal or ""
        self.authors = authors or ""
        self.first_author = first_author or ""
        self.year = year or ""
        self.source = source or ""
        self.bibtex = bibtex or ""

    def new_pdf_master_dict(self) -> dict:
        """
        Creates a dictionary representation of the PdfMaster instance, ready to be saved to the database.

        :returns: A dictionary containing the PDF master data.
        :rtype: dict
        """
        pdf_master_data = {
            "user_id": self.user_id,
            "path": self.path,
            "ref_count": 0,
            "hash": self.hash,
            "remote_faiss_path": self.remote_faiss_path,
            "remote_pkl_path": self.remote_pkl_path,
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