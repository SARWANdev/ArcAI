from bson import ObjectId

from database.repository.date_time_utils import get_utc_zulu_timestamp
from database.utils.mongo_connector import mongo_connection
from model.document_reader.pdf_master import PdfMaster
from services.bibtex_service import BibTeX_Service


class PdfMasterRepository:
    """
    Repository class for managing PDF master entries in MongoDB.

    Provides methods to create, read, update and delete metadata about PDF documents,
    including bibtex, author info, embedding paths, and usage counters.
    """
    def __init__(self, path: str):
        self.path = path

    @staticmethod
    def save(pdf: PdfMaster):
        """
        Saves a new PdfMaster document to the MongoDB collection.

        :param pdf: The PdfMaster instance containing the document metadata.
        :type pdf: PdfMaster

        :returns: The MongoDB ID of the saved document.
        :rtype: str
        """
        with mongo_connection() as db:
            pdf_master_id = db.pdf_master.insert_one(pdf.new_pdf_master_dict())
            return str(pdf_master_id.inserted_id)

    @staticmethod
    def delete_pdf_master(pdf_master_id) -> bool:
        """
        Deletes a PdfMaster document by its ID.

        :param pdf_master_id: The ID of the PdfMaster document to delete.
        :type pdf_master_id: str

        :returns: True if the document was deleted, False otherwise.
        :rtype: bool
        """
        try:
            with mongo_connection() as db:
                # Deletion in Mongo
                result = db.pdf_master.delete_one({"_id": ObjectId(pdf_master_id)})

                return result.deleted_count > 0
        except Exception as e:
            print(f"Pdf master could not be deleted: {e}")
            return False

    @staticmethod
    def increment_ref_count(pdf_master_id):
        """
        Increments the reference count for a PdfMaster document by 1.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str
        """
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$inc": {"ref_count": 1}})
        except Exception as e:
            print(f"count reference can not be incremented: {e}")

    @staticmethod
    def decrement_ref_count(pdf_master_id):
        """
        Decrements the reference count for a PdfMaster document by 1.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str
        """
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one(
                    {"_id": ObjectId(pdf_master_id)}, {"$inc": {"ref_count": -1}}  # Decrements by 1
                )
        except Exception as e:
            print(f"count reference could not be decremented: {e}")

    @staticmethod
    def get_ref_count(pdf_master_id):
        """
        Retrieves the reference count for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str

        :returns: The reference count of the document, or None if not found.
        :rtype: int | None
        """
        try:
            with mongo_connection() as db:
                ref_count = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"ref_count": 1}).get("ref_count")
                return ref_count
        except Exception as e:
            print(f"count reference could not be retrieved: {e}")
            return None

    @staticmethod
    def get_pdf_hash(pdf_master_id):
        """
        Retrieves the PDF hash for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str

        :returns: The hash of the document, or an empty string if not found.
        :rtype: str
        """
        try:
            with mongo_connection() as db:
                pdf_hash = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"hash": 1}).get("hash")
                return pdf_hash
        except Exception as e:
            print(f"hash can not be retrieved: {e}")
            return ""

    @staticmethod
    def get_path(pdf_master_id):
        """
        Retrieves the stored file path of the PDF.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str

        :returns: The path to the file if found, or empty string if not.
        :rtype: str
        """
        try:
            with mongo_connection() as db:
                path = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"path": 1}).get("path")
                return path
        except Exception as e:
            print(f"path can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_path(pdf_master_id, path):
        """
        Sets the file path for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str
        :param path: The new path to set for the document.
        :type path: str
        """
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"path": path}})
        except Exception as e:
            print(f"Failed to set path for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_vector_path(pdf_master_id):
        """
        Retrieves the vector store path for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str

        :returns: The path to the vector store if found, or an empty string if not.
        :rtype: str
        """
        try:
            with mongo_connection() as db:
                path = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"vector_store_path": 1}).get("vector_store_path")
                return path
        except Exception as e:
            print(f"vector store path can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_vector_path(pdf_master_id, new_vector_path):
        """
        Sets the vector store path for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str
        :param new_vector_path: The new vector store path to set for the document.
        :type new_vector_path: str
        """
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"vector_store_path": new_vector_path}})
        except Exception as e:
            print(f"Failed to set vector path for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_journal(pdf_master_id):
        """
        Retrieves the journal name for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str

        :returns: The journal name if found, or an empty string if not.
        :rtype: str
        """
        try:
            with mongo_connection() as db:
                journal = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"journal": 1}).get("journal")
                return journal
        except Exception as e:
            print(f"journal can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_journal(pdf_master_id, new_jornal):
        """
        Sets the journal name for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str
        :param new_jornal: The new journal name to set for the document.
        :type new_jornal: str
        """
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"journal": new_jornal}})
        except Exception as e:
            print(f"Failed to set journal for PDF {pdf_master_id}: {e}")

    @staticmethod
    def set_first_author(pdf_master_id, new_first_author):
        """
        Sets the first author for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str
        :param new_first_author: The new first author to set for the document.
        :type new_first_author: str

        """
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"first_author": new_first_author}})
        except Exception as e:
            print(f"Failed to set first author for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_first_author(pdf_master_id):
        """
        Retrieves the first author for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str

        :returns: The first author if found, or an empty string if not.
        :rtype: str
        """
        try:
            with mongo_connection() as db:
                author = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"first_author": 1}).get("first_author")
                return author
        except Exception as e:
            print(f"first author can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_year(pdf_master_id, new_year):
        """
        Sets the publication year for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str
        :param new_year: The new publication year to set for the document.
        :type new_year: str
        """
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"year": new_year}})
        except Exception as e:
            print(f"Failed to set year for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_year(pdf_master_id):
        """
        Retrieves the publication year for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str

        :returns: The publication year if found, or an empty string if not.
        :rtype: str
        """
        try:
            with mongo_connection() as db:
                year = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"year": 1}).get("year")
                return year
        except Exception as e:
            print(f"year can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_pages(pdf_master_id, new_pages):
        """
        Sets the page count for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str
        :param new_pages: The new page count to set for the document.
        :type new_pages: str
        """
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"pages": new_pages}})
        except Exception as e:
            print(f"Failed to set pages for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_pages(pdf_master_id):
        """
        Retrieves the page count for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str

        :returns: The page count if found, or an empty string if not.
        :rtype: str
        """
        try:
            with mongo_connection() as db:
                journal = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"pages": 1}).get("pages")
                return journal
        except Exception as e:
            print(f"pages can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_bibtex(pdf_master_id, new_bibtex ):
        """
        Sets the BibTeX entry for a PdfMaster document and updates associated metadata.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str
        :param new_bibtex: The new BibTeX string to set.
        :type new_bibtex: str
        """
        try:
            with mongo_connection() as db:
                bibtex_instance = BibTeX_Service().from_bibtex(new_bibtex)
                first_author = bibtex_instance.get_first_author()
                year = bibtex_instance.get_year()
                authors = bibtex_instance.get_authors()
                source = bibtex_instance.get_source()
                title = bibtex_instance.get_title()

                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"bibtex": new_bibtex, "year": year,
                                                                                     "source": source,
                                                                                     "authors": authors,
                                                                                     "first_author": first_author,
                                                                                     "title": title,
                                                                                     "updated_at": get_utc_zulu_timestamp()}})

        except Exception as e:
            print(f"Failed to set pages for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_bibtex(pdf_master_id):
        """
        Retrieves the BibTeX entry for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str

        :returns: The BibTeX string if found, or an empty string if not.
        :rtype: str
        """
        try:
            with mongo_connection() as db:
                bibtex = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"bibtex": 1}).get("bibtex")
                return bibtex
        except Exception as e:
            print(f"pages can not be retrieved: {e}")
            return ""

    @staticmethod
    def is_document_uploaded(pdf_hash: str, user_id):
        """
        Checks if a document with the given hash is already uploaded for the specified user.

        :param pdf_hash: The hash of the PDF to check.
        :type pdf_hash: str
        :param user_id: The ID of the user to check.
        :type user_id: str

        :returns: True if the document is uploaded, otherwise False.
        :rtype: bool
        """
        with mongo_connection() as db:
            result = db.pdf_master.find_one({"hash": pdf_hash, "user_id": user_id})
            return result


    @staticmethod
    def set_authors(pdf_master_id, new_authors):
        """
        Sets the authors for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str
        :param new_authors: The new authors to set for the document.
        :type new_authors: str
        """
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"authors": new_authors}})
        except Exception as a:
            print(f"Failed to set authors for PDF {pdf_master_id}: {a}")



    @staticmethod
    def get_authors(pdf_master_id):
        """
        Retrieves the authors for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str

        :returns: The authors if found, or an empty string if not.
        :rtype: str
        """
        try:
            with mongo_connection() as db:
                authors = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"authors": 1}).get("authors")
                return authors
        except Exception as e:
            print(f"authors can not be retrieved: {e}")
            return ""

    @staticmethod
    def get_source(pdf_master_id):
        """
        Retrieves the source for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str

        :returns: The source if found, or an empty string if not.
        :rtype: str
        """
        try:
            with mongo_connection() as db:
                source = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"source": 1}).get("source")
                return source
        except Exception as e:
            print(f"source can not be retrieved: {e}")
            return ""
        
    @staticmethod
    def set_source(pdf_master_id, new_source):
        """
        Sets the source for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str
        :param new_source: The new source to set for the document.
        :type new_source: str
        """
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"source": new_source}})
        except Exception as e:
            print(f"Failed to set source for PDF {pdf_master_id}: {e}")

    @staticmethod
    def set_remote_faiss_path(pdf_master_id, remote_faiss_path):
        """
        Sets the remote FAISS path for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str
        :param remote_faiss_path: The new remote FAISS path to set for the document.
        :type remote_faiss_path: str
        """
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"remote_faiss_path": remote_faiss_path}})
        except Exception as e:
            print(f"Failed to set faiss path for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_remote_faiss_path(pdf_master_id):
        """
        Retrieves the remote FAISS path for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str

        :returns: The remote FAISS path if found, or None if not.
        :rtype: str | None
        """
        try:
            with mongo_connection() as db:
                path = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"remote_faiss_path": 1}).get("remote_faiss_path")
                return path
        except Exception as e:
            print(f"Failed to get faiss path for PDF {pdf_master_id}: {e}")
            return None

    @staticmethod
    def set_remote_pkl_path(pdf_master_id, remote_pkl_path):
        """
        Sets the remote PKL path for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str
        :param remote_pkl_path: The new remote PKL path to set for the document.
        :type remote_pkl_path: str
        """
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)},
                                         {"$set": {"remote_pkl_path": remote_pkl_path}})
        except Exception as e:
            print(f"Failed to set remote_pkl_path for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_remote_pkl_path(pdf_master_id):
        """
        Retrieves the remote PKL path for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str

        :returns: The remote PKL path if found, or None if not.
        :rtype: str | None
        """
        try:
            with mongo_connection() as db:
                path = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"remote_pkl_path": 1}).get("remote_pkl_path")
                return path
        except Exception as e:
            print(f"Failed to get remote_pkl_path for PDF {pdf_master_id}: {e}")
            return None

    @staticmethod
    def get_user_id(pdf_master_id):
        """
        Retrieves the user ID for a PdfMaster document.

        :param pdf_master_id: The ID of the PdfMaster document.
        :type pdf_master_id: str

        :returns: The user ID if found, or None if not.
        :rtype: str | None
        """
        try:
            with mongo_connection() as db:
                user_id = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"user_id": 1}).get("user_id")
                return user_id
        except Exception as e:
            print(f"Failed to get user_id for PDF {pdf_master_id}: {e}")
            return None
