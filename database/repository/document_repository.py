from database.repository.date_time_utils import get_utc_zulu_timestamp
from database.utils.mongo_connector import mongo_connection
from typing import Optional, Dict
from utils.db_setup import es


class Document:
    def __init__(self, project_id: str, name: str, note: Optional[str] = None,
                  tag: Optional[str] = None, tag_color: Optional[str] = None):

        self.project_id = project_id
        self.pdf_master_id = None #TODO make the manager method for this attribute
        self.name = name
        self.note = note
        self.tag = tag
        self.tag_color = tag_color

        self.created_at = get_utc_zulu_timestamp()
        self.updated_at = self.created_at


    def new_document(self):
        document_data = {
            "project_id": self.project_id,
            "name": self.name,
            "note": self.note,
            "tag": self.tag,
            "tag_color": self.tag_color,
            "read": False,
            "favorite": False,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        with mongo_connection() as db:
            result = db.documents.insert_one(document_data)
            # Add document to Elasticsearch
            document_id = result.inserted_id
            es.index("documents", id=document_id, body={
                "title": self.name,
                "author": self.first_author, #TODO(Dani) this variables doesnt exist anymore in document, they are gonna be in pdf_master_repository
                "journal": self.journal,
                "suggest": {
                    "input": [self.name, self.author]
                }
            })
            return document_id
        


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
                #Update in Mongo
                result = db.documents.update_one({"_id": document_id},
                                        {"$set": {"name": name, "updated_at": get_utc_zulu_timestamp()}})
                #Update in Elastic
                es.update(index = "documents", id = document_id, body={
                    "doc": {"title": name}
                })
                return result.modified_count > 0
        except Exception as e:
            print(f"Document name could not be update: {e}")
            return False

    @staticmethod
    def delete_document(document_id) -> bool:
        try:
            with mongo_connection() as db:
                #Deletion in Mongo
                result = db.documents.delete_one({"_id": document_id})
                #Deletion in Mongo
                es.delete(index = "documents", id=document_id)
                return result.deleted_count > 0
        except Exception as e:
            print(f"Document could not be deleted: {e}")
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
        
    @staticmethod
    def get_pdf(document_id, path):
        #Gets a document's pdf to be downloaded or shown
        #TODO: finish this
        pass

        
    @staticmethod
    def search_documents(self, prefix):
        #Searches for documents in the database
        found = es.search(index="documents", body={
            "suggest": {
                "documents-suggest": {
                    "prefix": prefix,
                    "completion": {
                        "field": "suggest",
                        "size": 5
                    }
                }
            }
        })
        suggestions = found["suggest"]["documents-suggest"][0]["options"]
        document_ids = [suggestion["_id"] for suggestion in suggestions]
        result = []
        for id in document_ids:
            document = self.get_document_by_id(id)
            result.append(document)
        return result

