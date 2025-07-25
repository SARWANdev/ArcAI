from bson import ObjectId

from database.repository.date_time_utils import get_utc_zulu_timestamp
from database.utils.mongo_connector import mongo_connection
from typing import Dict
from database.repository.pdf_master_repository import PdfMasterRepository

from database.utils.db_setup import es

from model.document_reader.document import Document


class DocumentRepository:
    """
    A database handler for document operations.
    Provides CRUD, search, and metadata management
    for documents across MongoDB and Elasticsearch.
    Maintains sync between both databases.
    Static methods only - no instance needed.
    """

    @staticmethod
    def save(document: Document) -> str:
        """
        Saves a document to MongoDB and returns its ID.

        :param document: Instance of Document class.
        :type document: Document

        :return: The document ID.
        :rtype: str

        """
        with mongo_connection() as db:
            result = db.documents.insert_one(document.new_document_dict())
            doc_id = result.inserted_id
            return str(doc_id)

    @staticmethod
    def save_elastic(doc_id, text):
        """
        Indexes document in Elasticsearch with metadata and search suggestions.

        :param doc_id: ID of document.

        :param text: Text chunks to save
        """
        doc_id = str(doc_id)
        name = DocumentRepository.get_name(doc_id)
        author = DocumentRepository.get_authors(doc_id)
        es.index(index="documents", id=doc_id, body={
            "user_id": DocumentRepository.get_user_id(doc_id),
            "name": name,
            "author": author,
            "text": text, 
            "suggest": {"input": [name, author]}
        })

    @staticmethod
    def get_path(document_id):
        """
        Returns file path for the given document ID.

        :param document_id: ID of document.

        :return: Path to file.
        """
        pdf_master_id = DocumentRepository.get_pdf_master_id(document_id)
        return PdfMasterRepository.get_path(pdf_master_id)

    @staticmethod
    def get_year(document_id):
        """
        Returns publication year for the given document ID.

        :param document_id: ID of document.

        :return: Year of publication.
        """
        pdf_master_id = DocumentRepository.get_pdf_master_id(document_id)
        return PdfMasterRepository.get_year(pdf_master_id)

    @staticmethod
    def get_authors(document_id):
        """
        Returns authors list for the given document ID.

        :param document_id: ID of document.

        :return: String of authors.
        """
        pdf_master_id = DocumentRepository.get_pdf_master_id(document_id)
        return PdfMasterRepository.get_authors(pdf_master_id)

    @staticmethod
    def get_source(document_id):
        """
        Returns source/publication for the given document ID.

        :param document_id: ID of a document.

        :return: String of a source.
        """
        pdf_master_id = DocumentRepository.get_pdf_master_id(document_id)
        return PdfMasterRepository.get_source(pdf_master_id)

    @staticmethod
    def get_name(document_id):
        """
        Returns document name for the given ID.

        :param document_id: ID of a document.

        :return: String of document name.
        """
        with mongo_connection() as db:
            return db.documents.find_one({"_id": ObjectId(document_id)}, {"name": 1}).get("name")

    @staticmethod
    def set_pdf_master_id(document_id, pdf_master_id):
        """
        Links document to its PDF master record in MongoDB.

        :param document_id: ID of a document.

        :param pdf_master_id: ID of the PDF master record.
        """
        try:
            with mongo_connection() as db:
                db.documents.update_one({"_id": ObjectId(document_id)}, {"$set": {"pdf_master_id": pdf_master_id}})
        except Exception as e:
            print(f"pdf_master_id could not be set {e}")

    @staticmethod
    def get_pdf_master_id(document_id):
        """
        Return all documents belonging to a specific project.
        
        :param document_id: ID of a document.

        :return: ID of a documents belonging to a specific master.
        """
        with mongo_connection() as db:
            pdf_master_id = db.documents.find_one({"_id": ObjectId(document_id)}, {"pdf_master_id": 1}).get("pdf_master_id")
            return pdf_master_id

    @staticmethod
    def get_documents_by_project(project_id) -> list[Dict]:
        with mongo_connection() as db:
            return list(db.documents.find({"project_id": project_id}))


    @staticmethod
    def get_by_document_id(document_id) -> dict:
        """
        Returns complete document data for the given ID.

        :param document_id: ID of a document.

        :return: Dict of document data.
        """
        with mongo_connection() as db:
            return db.documents.find_one({"_id": ObjectId(document_id)})

    @staticmethod
    def update_document_name(document_id, name) -> bool:
        """
        Updates document name in both MongoDB and Elasticsearch.
        
        :param document_id: ID of a document.
        :param name: new name to be updated.

        :return: True if the name was updated.
        """
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
        """
        Deletes document from both MongoDB and Elasticsearch.

        :param document_id: ID of a document.

        :return: True if deleted.
        """
        try:
            with mongo_connection() as db:
                #Deletion in Mongo
                result = db.documents.delete_one({"_id": ObjectId(document_id)})
                #Deletion in Elasticsearch
                es.delete(index = "documents", id=document_id)
                return result.deleted_count > 0
        except Exception as e:
            print(f"Document could not be deleted: {e}")
            return False

    @staticmethod
    def get_note(document_id):
        """
        Returns note associated with the document.

        :param document_id: ID of a document.

        :return: String of note.
        """
        with mongo_connection() as db:
            note = db.documents.find_one({"_id": ObjectId(document_id)}, {"note": 1}).get("note")
            return note

    @staticmethod
    def get_bibtex_by_document_id(document_id) -> str:
        """
        Returns BibTeX reference for the document.

        :param document_id: ID of a document.

        :return: String of BibTeX reference.
        """
        try:
            with mongo_connection() as db:
                return db.documents.find_one({"_id": ObjectId(document_id)})["bibtex"]
        except Exception as e:
            print(f"Bibtex could not be retrieved: {e}")
            return str()

    @staticmethod
    def search_documents(user_id, query):
        """
        Searches documents by name/author for given user with prefix matching.

        :param user_id: ID of user.
        :type user_id: str
        :param query: Search query.
        :type query: str

        :return: List of documents.
        :rtype: list[dics]
        """
        es.indices.refresh(index="documents")
        result = es.search(index="documents", body={
            "size": 5, 
            "query": {
                "bool": {
                    "should": [
                        # Autocomplete by name
                        {
                            "match_phrase_prefix": {
                                "name": {
                                    "query": query
                                }
                            }
                        },
                        # Autocomplete by author
                        {
                            "match_phrase_prefix": {
                                "author": {
                                    "query": query
                                }
                            }
                        }
                    ],
                    "filter": [
                        { "term": { "user_id": user_id } }
                    ],
                    "minimum_should_match": 1 
                }
            }
        })
        hits = result["hits"]["hits"]
        return [
            {"id": hit["_id"], "name": hit["_source"].get("name", ""), "author": hit["_source"].get("author", "")}
            for hit in hits
        ]

    @staticmethod
    def search_contents(user_id, query):
        """
        Searches document contents with fuzzy matching for given user.

        :param user_id: ID of user.
        :type user_id: str
        :param query: Search query.
        :type query: str

        :return: List of hit documents.
        :rtype: list[dict]
        """
        es.indices.refresh(index="documents")
        result = es.search(index="documents", body={
            "size": 5,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "text": {
                                    "query": query,
                                    "operator": "and",
                                    "fuzziness": "AUTO"
                                }
                            }
                        }
                    ],
                    "filter": [
                        {
                            "term": {
                                "user_id": user_id
                            }
                        }
                    ]
                }
            }
        })

        hits = result["hits"]["hits"]
        return [
            {"id": hit["_id"], "name": hit["_source"].get("name", ""), "author": hit["_source"].get("author", ""), "text": hit["_source"].get("text", "")}
            for hit in hits
        ]
    
    
    @staticmethod
    def get_user_id(document_id):
        """
        Returns owner user ID for the given document.

        :param document_id: ID of a document.

        :return: ID of owner user.
        """
        pdf_master_id = DocumentRepository.get_pdf_master_id(document_id)
        return PdfMasterRepository.get_user_id(pdf_master_id)
