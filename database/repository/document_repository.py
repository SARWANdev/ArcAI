from bson import ObjectId

from database.repository.date_time_utils import get_utc_zulu_timestamp
from database.utils.mongo_connector import mongo_connection
from typing import Optional, Dict
from database.repository.pdf_master_repository import PdfMasterDataBase

from database.utils.db_setup import es

from model.document_reader.document import Document


class DocumentDataBase:

    # this method store an object Document and returns the Mong _id.
    @staticmethod
    def save(document: Document) -> str:
        with mongo_connection() as db:
            doc_id = db.documents.insert_one(document.new_document_dict())
            return str(doc_id.inserted_id)

    @staticmethod
    def get_year( document_id ):
        pdf_master_id = DocumentDataBase.get_pdf_master_id( document_id )
        return PdfMasterDataBase.get_year( pdf_master_id )

    @staticmethod
    def get_authors(document_id):
        pdf_master_id = DocumentDataBase.get_pdf_master_id(document_id)
        return PdfMasterDataBase.get_authors( pdf_master_id )

    @staticmethod
    def get_source( document_id ):
        pdf_master_id = DocumentDataBase.get_pdf_master_id( document_id )
        return PdfMasterDataBase.get_source( pdf_master_id )

    @staticmethod
    def get_name(document_id):
        with mongo_connection() as db:
            return db.documents.find_one({"_id": ObjectId(document_id)}, {"name": 1}).get("name")

    @staticmethod
    def set_pdf_master_id(document_id, pdf_master_id):
        try:
            with mongo_connection() as db:
                db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"pdf_master_id": pdf_master_id}})
        except Exception as e:
            print(f"pdf_master_id could not be set {e}")

    @staticmethod
    def get_pdf_master_id(document_id):
        with mongo_connection() as db:
            pdf_master_id = db.documents.find_one({"_id": ObjectId(document_id)}, {"pdf_master_id": 1}).get("pdf_master_id")
            return pdf_master_id

    @staticmethod
    def get_documents_by_project(project_id) -> list[Dict]:
        with mongo_connection() as db:
            return list(db.documents.find({"project_id": project_id}))


    @staticmethod
    def get_by_document_id(document_id) -> dict:
        with mongo_connection() as db:
            return db.documents.find_one({"_id": ObjectId(document_id)})

    @staticmethod
    def update_document_name(document_id, name) -> bool:
        try:
            with mongo_connection() as db:
                #Update in Mongo
                result = db.documents.update_one({"_id": ObjectId(document_id)},
                                        {"$set": {"name": name, "updated_at": get_utc_zulu_timestamp()}})
                #Update in Elastic
                es.update(index = "documents", id = document_id, body={
                    "doc": {"name": name}
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
                result = db.documents.delete_one({"_id": ObjectId(document_id)})
                #Deletion in Elastic search
                #es.delete(index = "documents", id=document_id)
                return result.deleted_count > 0
        except Exception as e:
            print(f"Document could not be deleted: {e}")
            return False

    @staticmethod
    def update_path(document_id, path) -> bool:
         try:
             with mongo_connection() as db:
                 result = db.documents.update_one({"_id": ObjectId(document_id)},
                                         {"$set": {"path": path, "updated_at": get_utc_zulu_timestamp()}})
                 return result.modified_count > 1
         except Exception as e:
             print(f"Document path could not be update: {e}")
             return False
        
    @staticmethod
    def update_vector_store_path(document_id, vector_store_path):
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)},
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
                return db.documents.find_one({"_id": ObjectId(document_id)})["bibtex"]
        except Exception as e:
            print(f"Bibtex could not be retrieved: {e}")
            return str()

    @staticmethod
    def update_bibtex(document_id, bibtex) -> bool:
        try:
            with mongo_connection() as db:
                result = db.documents.update_one({"_id": ObjectId(document_id)},
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

