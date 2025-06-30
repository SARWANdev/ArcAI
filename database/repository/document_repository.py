from database.repository.date_time_utils import get_utc_zulu_timestamp
from database.utils.mongo_connector import mongo_connection
from typing import Optional, Dict


class Document:
    def __init__(self, project_id: str, name: str, path: str, vector_store_path: str, note: Optional[str] = None,
                 journal: Optional[str] = None, author: Optional[str] = None, year: Optional[str] = None,
                 pages: Optional[int] = None, tag: Optional[str] = None, tag_color: Optional[str] = None,  bibtex = None):

        self.project_id = project_id
        self.name = name
        self.path = path
        self.vector_store_path = vector_store_path
        self.note = note
        self.read = False
        self.favorite = False
        self.journal = journal
        self.first_author = author
        self.year = year
        self.pages = pages
        self.tag = tag
        self.tag_color = tag_color
        self.bibtex = bibtex

        self.created_at = get_utc_zulu_timestamp()
        self.updated_at = self.created_at


    def new_document(self):
        document_data = {
            "project_id": self.project_id,
            "name": self.name,
            "path": self.path,
            "vector_store_path": self.vector_store_path,
            "note": self.note,
            "year": self.year,
            "pages": self.pages,
            "journal": self.journal,
            "first_author": self.first_author,
            "tag": self.tag,
            "tag_color": self.tag_color,
            "read": self.read,
            "favorite": self.favorite,
            "bibtex": self.bibtex,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        with mongo_connection() as db:
            db.documents.insert_one(document_data)


    @staticmethod
    def get_documents_by_project(project_id) -> list[Dict]:
        with mongo_connection() as db:
            return list(db.documents.find({"project_id": project_id}))


    @staticmethod
    def get_by_document_id(document_id) -> dict:
        with mongo_connection() as db:
            return db.documents.find_one({"_id": document_id})

    @staticmethod
    def update_document_name(document_id, name) -> bool:
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": document_id},
                                        {"$set": {"name": name, "updated_at": get_utc_zulu_timestamp()}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Document name could not be update: {e}")
            return False


    @staticmethod
    def update_path(document_id, path) -> bool:
         try:
             with mongo_connection() as db:
                 result = db.documents.update_one({"_id": document_id},
                                         {"$set": {"path": path, "updated_at": get_utc_zulu_timestamp()}})
                 return result.modified_count > 1
         except Exception as e:
             print(f"Document path could not be update: {e}")
             return False
        
    @staticmethod
    def update_vector_store_path(document_id, vector_store_path):
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": document_id},
                                        {"$set": {"vector_store_path": vector_store_path,
                                                  "updated_at": get_utc_zulu_timestamp()}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Embeddings path could not be update: {e}")
            return False

    @staticmethod
    def get_bibtex_by_document_id(document_id) -> str:
        try:
            with mongo_connection() as db:
                return db.documents.find_one({"_id": document_id})["bibtex"]
        except Exception as e:
            print(f"Bibtex could not be retrieved: {e}")
            return str()

    @staticmethod
    def update_bibtex(document_id, bibtex) -> bool:
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": document_id},
                                        {"$set": {"bibtex": bibtex,
                                                      "updated_at": get_utc_zulu_timestamp()}})
                return result.modified_count > 0
        except Exception as e:
            print(f"Bibtex could not be update: {e}")
            return False
