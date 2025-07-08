from database.utils.mongo_connector import mongo_connection
from services.upload_manager.document_upload_service import get_pdf_sha256


class PdfMaster:
    def __init__(self, path: str):
        self.path = path

    """
    This method creates a new instance in the collection pdf_master an returns the pdf_master id
    
    all the attributes for this collection are supposed to be constant and would apply for all instances of teh same document
    """

    def new_pdf_master(self):

        pdf_master_data = {
            "path": self.path,
            "ref_count": 0,
            "hash": get_pdf_sha256(self.path),
            "vector_store_path": "",
            "journal": "",
            "first_author": "",
            "year": None,
            "pages": None,
            "bibtex": None
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
    def get_ref_count(pdf_master_id):
        try:
            with mongo_connection() as db:
                ref_count = db.pdf_master.find({"_id": pdf_master_id}, {"ref_count": 1}).get("ref_count")
                return ref_count
        except Exception as e:
            print(f"count reference could not be retrieved: {e}")
            return None


    @staticmethod
    def get_pdf_hash(pdf_master_id):
        try:
            with mongo_connection() as db:
                pdf_hash = db.pdf_master.find_one({"_id": pdf_master_id}, {"hash": 1}).get("hash")
                return pdf_hash
        except Exception as e:
            print(f"hash can not be retrieved: {e}")
            return ""

    @staticmethod
    def get_path(pdf_master_id):
        try:
            with mongo_connection() as db:
                path = db.pdf_master.find_one({"_id": pdf_master_id}, {"path": 1}).get("path")
                return path
        except Exception as e:
            print(f"path can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_path(pdf_master_id, path):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": pdf_master_id}, {"$set": {"path": path}})
        except Exception as e:
            print(f"Failed to set path for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_vector_path(pdf_master_id):
        try:
            with mongo_connection() as db:
                path = db.pdf_master.find_one({"_id": pdf_master_id}, {"vector_store_path": 1}).get("vector_store_path")
                return path
        except Exception as e:
            print(f"vector store path can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_vector_path(pdf_master_id, new_vector_path):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": pdf_master_id}, {"$set": {"vector_store_path": new_vector_path}})
        except Exception as e:
            print(f"Failed to set vector path for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_journal(pdf_master_id):
        try:
            with mongo_connection() as db:
                journal = db.pdf_master.find_one({"_id": pdf_master_id}, {"journal": 1}).get("journal")
                return journal
        except Exception as e:
            print(f"journal can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_journal(pdf_master_id, new_jornal):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": pdf_master_id}, {"$set": {"journal": new_jornal}})
        except Exception as e:
            print(f"Failed to set journal for PDF {pdf_master_id}: {e}")

    @staticmethod
    def set_first_author(pdf_master_id, new_first_author):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": pdf_master_id}, {"$set": {"first_author": new_first_author}})
        except Exception as e:
            print(f"Failed to set first author for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_first_author(pdf_master_id):
        try:
            with mongo_connection() as db:
                author = db.pdf_master.find_one({"_id": pdf_master_id}, {"first_author": 1}).get("first_author")
                return author
        except Exception as e:
            print(f"first author can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_year(pdf_master_id, new_year):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": pdf_master_id}, {"$set": {"year": new_year}})
        except Exception as e:
            print(f"Failed to set year for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_year(pdf_master_id):
        try:
            with mongo_connection() as db:
                year = db.pdf_master.find_one({"_id": pdf_master_id}, {"year": 1}).get("year")
                return year
        except Exception as e:
            print(f"year can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_pages(pdf_master_id, new_pages):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": pdf_master_id}, {"$set": {"pages": new_pages}})
        except Exception as e:
            print(f"Failed to set pages for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_pages(pdf_master_id):
        try:
            with mongo_connection() as db:
                journal = db.pdf_master.find_one({"_id": pdf_master_id}, {"pages": 1}).get("pages")
                return journal
        except Exception as e:
            print(f"pages can not be retrieved: {e}")
            return ""

    @staticmethod
    def set_bibtex(pdf_master_id, new_bibtex):
        try:
            with mongo_connection() as db:
                db.pdf_master.update_one({"_id": pdf_master_id}, {"$set": {"bibtex": new_bibtex}})
        except Exception as e:
            print(f"Failed to set pages for PDF {pdf_master_id}: {e}")

    @staticmethod
    def get_bibtex(pdf_master_id):
        try:
            with mongo_connection() as db:
                bibtex = db.pdf_master.find_one({"_id": pdf_master_id}, {"bibtex": 1}).get("bibtex")
                return bibtex
        except Exception as e:
            print(f"pages can not be retrieved: {e}")
            return ""

    @staticmethod
    def is_document_uploaded(pdf_hash: str):
        with mongo_connection() as db:
            result = db.pdf_master.find_one({"hash": pdf_hash})
            return result




"""
DUMMY TEST TO UNDERTSAND ; NOT IMPORTANT

def test_pdfmaster_operations():
    from bson import ObjectId  # For simulating existing IDs if needed

    # 1. Create a new PDF master entry
    print("=== Creating new PDF master ===")
    fake_path = r"C:\Users\User\Documents\formulario alicacion mama.pdf"
    pdf = PdfMaster(fake_path)
    pdf_id = pdf.new_pdf_master()
    print(f"Created PDF master with ID: {pdf_id}")

    # If you want to test with an existing ID (for get/update methods), uncomment:
    # pdf_id = ObjectId("507f1f77bcf86cd799439011")  # Fake existing ID

    # 2. Get the PDF hash
    print("\n=== Getting PDF hash ===")
    pdf_hash = PdfMaster.get_pdf_hash(pdf_id)
    print(f"PDF hash: {pdf_hash if pdf_hash else '<not found>'}")

    # 3. Increment ref count
    print("\n=== Incrementing ref count ===")
    PdfMaster.increment_ref_count(pdf_id)
    print(f"Incremented ref_count for {pdf_id}")

    # 3. Increment ref count
    print("\n=== Incrementing ref count ===")
    PdfMaster.increment_ref_count(pdf_id)
    print(f"Incremented ref_count for {pdf_id}")

    # 3. Increment ref count
    print("\n=== Incrementing ref count ===")
    PdfMaster.increment_ref_count(pdf_id)
    print(f"Incremented ref_count for {pdf_id}")

    # 3. Increment ref count
    print("\n=== Incrementing ref count ===")
    PdfMaster.increment_ref_count(pdf_id)
    print(f"Incremented ref_count for {pdf_id}")

    # 4. Decrement ref count
    print("\n=== Decrementing ref count ===")
    PdfMaster.decrement_ref_count(pdf_id)
    print(f"Decremented ref_count for {pdf_id}")

    # 4. Decrement ref count
    print("\n=== Decrementing ref count ===")
    PdfMaster.decrement_ref_count(pdf_id)
    print(f"Decremented ref_count for {pdf_id}")

    # 5. Update path
    print("\n=== Updating path ===")
    new_path = "/new/fake/path/updated.pdf___"
    PdfMaster.set_path(pdf_id, new_path)
    print(f"Updated path to: {new_path}")

    # Verification (simplified - would query DB in real use)
    print("\n=== Final state (simulated) ===")
    print(f"ID: {pdf_id}")
    print(f"Path: {new_path}")
    print(f"Hash: {pdf_hash}")
    print("ref_count: 0 (initial 0 +1 -1)")
    return pdf_id


if __name__ == "__main__":
    pdf_id = test_pdfmaster_operations()
    print("======HASH=========")
    print("===============")
    print(PdfMaster.get_pdf_hash(pdf_id))
    print("===============")

    print("======Path=========")
    print("===============")
    print(PdfMaster.get_path(pdf_id))
    print("===============")

"""




