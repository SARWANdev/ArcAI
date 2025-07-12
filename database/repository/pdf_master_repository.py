from bson import ObjectId

from database.utils.mongo_connector import mongo_connection
from model.document_reader.pdf_master import PdfMaster


class PdfMasterDataBase:
    def __init__(self, path: str):
        self.path = path

    @staticmethod
    def save(pdf: PdfMaster):
        with mongo_connection() as db:
            pdf_master_id = db.pdf_master.insert_one(pdf.new_pdf_master_dict())
            return str(pdf_master_id.inserted_id)

    @staticmethod
    def delete_pdf_master(pdf_master_id) -> bool:
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
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$inc": {"ref_count": 1}})
        except Exception as e:
            print(f"count reference can not be incremented: {e}")

    @staticmethod
    def decrement_ref_count(pdf_master_id):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one(
                    {"_id": ObjectId(pdf_master_id)}, {"$inc": {"ref_count": -1}}  # Decrements by 1
                )
        except Exception as e:
            print(f"count reference could not be decremented: {e}")

    @staticmethod
    def get_ref_count(pdf_master_id):
        try:
            with mongo_connection() as db:
                ref_count = db.pdf_master.find({"_id": ObjectId(pdf_master_id)}, {"ref_count": 1}).get("ref_count")
                return ref_count
        except Exception as e:
            print(f"count reference could not be retrieved: {e}")
            return None


    @staticmethod
    def get_pdf_hash(pdf_master_id):
        try:
            with mongo_connection() as db:
                pdf_hash = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"hash": 1}).get("hash")
                return pdf_hash
        except Exception as e:
            print(f"hash can not be retrieved: {e}")
            return ""

    @staticmethod
    def get_path(pdf_master_id):
        try:
            with mongo_connection() as db:
                path = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"path": 1}).get("path")
                return path
        except Exception as e:
            print(f"path can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_path(pdf_master_id, path):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"path": path}})
        except Exception as e:
            print(f"Failed to set path for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_vector_path(pdf_master_id):
        try:
            with mongo_connection() as db:
                path = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"vector_store_path": 1}).get("vector_store_path")
                return path
        except Exception as e:
            print(f"vector store path can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_vector_path(pdf_master_id, new_vector_path):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"vector_store_path": new_vector_path}})
        except Exception as e:
            print(f"Failed to set vector path for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_journal(pdf_master_id):
        try:
            with mongo_connection() as db:
                journal = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"journal": 1}).get("journal")
                return journal
        except Exception as e:
            print(f"journal can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_journal(pdf_master_id, new_jornal):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"journal": new_jornal}})
        except Exception as e:
            print(f"Failed to set journal for PDF {pdf_master_id}: {e}")

    @staticmethod
    def set_first_author(pdf_master_id, new_first_author):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"first_author": new_first_author}})
        except Exception as e:
            print(f"Failed to set first author for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_first_author(pdf_master_id):
        try:
            with mongo_connection() as db:
                author = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"first_author": 1}).get("first_author")
                return author
        except Exception as e:
            print(f"first author can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_year(pdf_master_id, new_year):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"year": new_year}})
        except Exception as e:
            print(f"Failed to set year for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_year(pdf_master_id):
        try:
            with mongo_connection() as db:
                year = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"year": 1}).get("year")
                return year
        except Exception as e:
            print(f"year can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_pages(pdf_master_id, new_pages):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"pages": new_pages}})
        except Exception as e:
            print(f"Failed to set pages for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_pages(pdf_master_id):
        try:
            with mongo_connection() as db:
                journal = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"pages": 1}).get("pages")
                return journal
        except Exception as e:
            print(f"pages can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_bibtex(pdf_master_id, new_bibtex):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": ObjectId(pdf_master_id)}, {"$set": {"bibtex": new_bibtex}})
        except Exception as e:
            print(f"Failed to set pages for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_bibtex(pdf_master_id):
        try:
            with mongo_connection() as db:
                bibtex = db.pdf_master.find_one({"_id": ObjectId(pdf_master_id)}, {"bibtex": 1}).get("bibtex")
                return bibtex
        except Exception as e:
            print(f"pages can not be retrieved: {e}")
            return ""

    @staticmethod
    def is_document_uploaded(pdf_hash: str, user_id):
        with mongo_connection() as db:
            result = db.pdf_master.find_one({"hash": pdf_hash, "user_id": user_id})
            return result







