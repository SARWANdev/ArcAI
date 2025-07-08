from database.utils.mongo_connector import mongo_connection
from typing import Optional, Dict

from services.upload_manager.document_upload_service import get_pdf_sha256


class Pdfmaster:
    def __init__(self, path: str):
        self.path = path

    """
    This method creates a new instance in the collection pdf_master an returns the pdf_master id
    """

    def new_pdf_master(self):

        pdf_master_data = {
            "path": self.path,
            "ref_count": 0,
            "hash": get_pdf_sha256(self.path)
        }

        with mongo_connection() as db:
            result = db.pdf_master.insert_one(pdf_master_data)

        return result.inserted_id

    @staticmethod
    def increment_ref_count(pdf_master_id):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": pdf_master_id}, {"$inc": {"ref_count": 1}})
        except Exception as e:
            print(f"count reference can not be incremented: {e}")

    @staticmethod
    def decrement_ref_count(pdf_master_id):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one(
                    {"_id": pdf_master_id}, {"$inc": {"ref_count": -1}}  # Decrements by 1
                )
        except Exception as e:
            print(f"count reference could not be decremented: {e}")

    @staticmethod
    def get_pdf_hash(pdf_master_id: str) -> str:
        """Retrieve the PDF hash from MongoDB by its master ID.

        Args:
            pdf_master_id: The MongoDB _id of the PDF document.

        Returns:
            The PDF hash as a string, or an empty string if not found/error occurs.
        """
        try:
            with mongo_connection() as db:
                document = db.conversations.find_one(
                    {"_id": pdf_master_id},
                    {"hash": 1}  # Projection: Only fetch the 'hash' field
                )
                return document.get("hash", "") if document else ""
        except Exception as e:
            print(f"Failed to retrieve hash for PDF {pdf_master_id}: {e}")
            return ""

    @staticmethod
    def set_path(pdf_master_id, path):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": pdf_master_id}, {"$set": {"path": path}})
        except Exception as e:
            print(f"Failed to set path for PDF {pdf_master_id}: {e}")



