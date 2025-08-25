import os
import tempfile
from database.repository.document_repository import DocumentRepository
from database.repository.document_properties_repository import DocumentPropertiesRepository
from database.repository.pdf_master_repository import PdfMasterRepository
from database.repository.tag_registry_repository import TagRegistryRepository
from database.repository.conversation_repository import ConversationRepository
from database.repository.project_repository import Project as ProjectRepository
from exceptions.document_exceptions import InvalidServerConnectionException
from exceptions.tag_exceptions import TagException, InvalidTagName, MissingTagColor

from model.document_reader.document import Document as DocumentModel
from model.document_reader.pdf_master import PdfMaster as PdfMasterModel
from model.document_reader.tag_manager.tag import Tag as TagModel

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from services.ai_service import AIService
from services.bibtex_service import BibTeX_Service
from services.conversation_service import ConversationService

from services.upload_manager.hash_manager import get_pdf_sha256, relative_path_generator
from services.upload_manager.embeddings_manager import EmbeddingsManager
from services.upload_manager.server_conection import upload_document, delete_remote_directory, save_embeddings
from services.notebook_service import NotebookService
from validators.document_validator import DocumentValidator

from database.utils.mongo_connector import mongo_connection


class DocumentService:

    """Service layer for document management operations.

    Handles:
    - Document uploads and deduplication (hash-based)
    - PDF text/metadata extraction and chunking
    - Elasticsearch indexing and search
    - Document CRUD operations
    - Tag management
    - Document state management (read/favorite)
    - Project-based document organization
    - Embeddings generation and storage

    Dependencies:
    - MongoDB repositories for persistence
    - Elasticsearch for text search
    - PDF processing libraries
    - AI services for embeddings
    """

    def __init__(self):
        self.document_repository = DocumentRepository 
        self.document_properties_repo = DocumentPropertiesRepository
        self.conversation_repository = ConversationRepository
        self.pdf_master_repository = PdfMasterRepository
        self.notebook_service = NotebookService()
        self.ai_service = AIService()

    def upload_file(self, file, user_id, project_id):
        """
        Uploads a file to storage and creates document record.

        :param file: File object to upload
        :param user_id: Owner user ID
        :param project_id: Target project ID
        :return: None
        """

        DocumentValidator.validate_file(file)
        DocumentValidator.validate_user_id(user_id)
        DocumentValidator.validate_project_id(project_id)

        original_name = file.filename
        suffix = "." + file.filename.split(".")[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
        self.__upload_document(document_path = tmp_path, user_id = user_id, project_id = project_id, original_name=original_name)
        os.remove(tmp_path)

    def get_document(self, document_id):
        """
        Retrieves and constructs a DocumentModel from a database by ID.

        :param document_id: The ID of the document to retrieve
        :return: DocumentModel instance or None if not found
        """
        # Retrieve document data from the database
        document_data = self.document_repository.get_by_document_id(document_id)
        if not document_data:
            return None

        document_model = DocumentModel(
            document_id=document_id,
            name=document_data.get('name'),
            project_id=document_data.get('project_id'),
            pdf_master_id=document_data.get('pdf_master_id'),
            note=document_data.get('note'),
            tag_name=document_data.get('tag_name'),
            tag_color=document_data.get('tag_color'),
            read=document_data.get('read'),
            favorite=document_data.get('favorite'),
            created_at=document_data.get('created_at'),
            updated_at=document_data.get('updated_at')
        )

        # Update state using explicit methods
        if document_data.get('read'):
            document_model.mark_read()
        else:
            document_model.mark_unread()

        if document_data.get('favorite'):
            document_model.add_favorite()
        else:
            document_model.remove_favorite()

        tag_name = document_data.get('tag_name')
        tag_color = document_data.get('tag_color')
        if tag_name is not None and tag_color is not None and tag_name.strip() and tag_color.strip():
            tag_obj = TagModel(tag_name, tag_color)
            document_model.set_tag(tag_obj)

        return document_model

    def get_project_documents(self, project_id):
        """
        Retrieves all documents belonging to a project.

        :param project_id: ID of the project to fetch documents for
        :return: List[DocumentModel] if documents exist, None otherwise
        """
        documents_data = self.document_repository.get_documents_by_project(project_id)
        if not documents_data:
            return None
        documents_list = []
        for document_data in documents_data:
            doc_id = document_data.get('_id')
            document_model = self.get_document(doc_id)
            if document_model:
                documents_list.append(document_model)
        return documents_list

    def add_tag(self, document_id, tag_name, tag_color, user_id, project_id):
        """
        Adds a tag to the specified document.

        :param document_id: Unique identifier of the target document
        :param tag_name: Name of the tag to be added
        :param tag_color: Color code for the tag (hex or named color)
        :return: True if tag was successfully added, False otherwise
        :raises InvalidTagName: If the tag name is invalid
        :raises MissingTagColor: If the tag color is missing or invalid
        :raises TagException: If there's a conflict with existing tag colors
        """
        try:
            tag_obj = TagModel(tag_name, tag_color)
            tag_name = tag_obj.get_name()
            tag_color = tag_obj.get_color()

            existing_tag = TagRegistryRepository.get_tag(tag_name, user_id, project_id)
            if existing_tag:
                if existing_tag["color"] != tag_color:
                    return False
                    #raise TagException(f"Tag with name '{tag_name}' already exists with a different color.")

            else:
                TagRegistryRepository.create_or_verify_tag(tag_name, tag_color, user_id, project_id)

            success_name = self.document_properties_repo.update_tag(document_id, tag_name)
            success_color = self.document_properties_repo.update_tag_color(document_id, tag_color)
            return success_name and success_color
            
        except (InvalidTagName, MissingTagColor, TagException):
            # Re-raise these exceptions as they are already properly formatted
            raise
        except Exception as e:
            # Handle any other unexpected errors
            print(f"Unexpected error while adding tag: {e}")
            return False

    def __create_document(self, document_name, project_id, pdf_master_id) -> str:
        """
        Create a new document in the system with associated components.

        :param document_name: The given name of the document.
        :param project_id: ID of the project this document belongs to.
        :param pdf_master_id: ID of the master PDF file this document is based on.
        :return: The newly created document ID.
        """
        new_name = self.__rename_according_ref_count(document_name, pdf_master_id)
        new_document_instance = DocumentModel(name = new_name,
                                              project_id = project_id,
                                              pdf_master_id = pdf_master_id)
        new_document_id = self.document_repository.save(new_document_instance)
        user_id = ProjectRepository.get_user_id(project_id)
        ConversationService().create_document_conversation(user_id, document_id=new_document_id)
        self.pdf_master_repository.increment_ref_count(pdf_master_id)
        
        # Don't call notebook service here - the note field is already set to "" in new_document_dict()
        # The notebook will be created automatically with the document

        return new_document_id
    


    def __create_pdf_master(self, document_path, user_id, project_id, pdf_hash, original_name) -> str:
        """
        Creates and stores a master PDF record in the system with metadata extraction.

        :param document_path: Remote filesystem path where the PDF is temporarily stored
        :param user_id: ID of the user who owns this document
        :param project_id: ID of the project, this document belongs to
        :param pdf_hash: Unique hash of the PDF file content
        :param original_name: Original filename as uploaded by the use
        :return: The newly created PDF master record ID
        """
        relative_path = relative_path_generator(user_id, project_id)
        bibtex_instance = BibTeX_Service(paper_name=original_name, pdf_hash=pdf_hash)
        bibtex_str = bibtex_instance.formatted_bibtex_string
        pdf_path_in_server = upload_document(local_path = document_path, relative_path = relative_path, pdf_hash = pdf_hash)
        new_pdf_master_instance = PdfMasterModel(path = pdf_path_in_server, pdf_hash = pdf_hash, user_id = user_id,
                                                 year = bibtex_instance.get_year(), source = bibtex_instance.get_source(),
                                                 authors = str(bibtex_instance.get_authors()), bibtex= bibtex_str,
                                                 first_author= bibtex_instance.get_first_author(),)

        pdf_master_id = self.pdf_master_repository.save(new_pdf_master_instance)
        return pdf_master_id

    def get_first_author(self, document_id):
        """
        Retrieves the first author from the document.

        :param document_id: The ID of the document to retrieve the first author from.
        :return: String or None
        """
        return self.document_properties_repo.get_first_author(document_id)



    def __embeddings_storage(self, document_path, pdf_master_id):
        """
        Generate and store embeddings for the document.

        :param document_path: Path to the document file to process
        :param pdf_master_id: ID of the associated PDF master record
        :return:
        """
        try:
            text_chunks = self.__get_text_chunks(document=document_path)
            embeddings = self.ai_service.get_vector_store(text_chunks=text_chunks)
            serialized_vector_store = EmbeddingsManager.serialize_vector_store(embeddings)
            path_in_server = self.pdf_master_repository.get_path(pdf_master_id)
            paths = save_embeddings(path_in_server, serialized_vector_store[0], serialized_vector_store[1])
            self.pdf_master_repository.set_remote_faiss_path(pdf_master_id, paths[0])
            self.pdf_master_repository.set_remote_pkl_path(pdf_master_id, paths[1])
            return True
        except Exception:
            #raise AIEmbeddingException("Rolling back changes.") from e
            return False





    def __upload_document(self, document_path: str, user_id: str, project_id: str, original_name: str):
        """
        Handles document deduplication via hash checks, creates necessary database records,
        generates embeddings, and indexes the text content.

        :param document_path: Local filesystem path to the PDF document
        :param user_id: Owner of the document
        :param project_id: Target project for upload
        :param original_name: Original filename from uploader
        """

        pdf_hash = get_pdf_sha256(document_path)
        existing_pdf_master = self.pdf_master_repository.is_document_uploaded(pdf_hash, user_id)
        success_embeddings = False
        server_success = True

        if existing_pdf_master:
            pdf_master_id = str(existing_pdf_master.get("_id"))
            success_embeddings = True
        else:

            try:
                pdf_master_id = self.__create_pdf_master(document_path, user_id, project_id, pdf_hash, original_name)
                success_embeddings = self.__embeddings_storage(document_path, pdf_master_id)
                print("pdf_master_id: " + pdf_master_id)
            except InvalidServerConnectionException as e:
                server_success = False

        document_id = self.__create_document(original_name, project_id, pdf_master_id)
        print("document_id: " + document_id)
        text = self.__get_pdf_text(document_path)
        elastic_success = DocumentRepository.save_elastic(document_id, text)

        if not success_embeddings or not server_success or not elastic_success:
            self.delete_document(document_id)
            raise InvalidServerConnectionException("Either server or Ai failed")



    def __get_pdf_text(self, document) -> str:
        """
        Extracts and concatenates text from all pages of a PDF document.

        :param document: PDF file path or file-like object to read from
        :return: str: Extracted text from all PDF pages concatenated
        """
        pdf_reader = PdfReader(document) #can also take a document path
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        return text
    
    def __get_pdf_metadata(self, document:str):
        """
        Extracts PDF metadata and splits text into chunks with metadata prepended.

        :param document: Path to the PDF file
        :return: List of text chunks with metadata as first element
        """
        pdf_reader = PdfReader(document)
        metadata = pdf_reader.metadata
        return metadata

    def __get_text_chunks(self, document) -> list[str]:
        """
        Splits PDF text into chunks with metadata.

        :param document: PDF document to process
        :return:  List of text chunks with metadata as first element
        """
        metadata = str(self.__get_pdf_metadata(document=document))
        text = self.__get_pdf_text(document)
        text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
        )
    
        chunks = text_splitter.split_text(text)
        chunks.insert(0, metadata)
        return chunks

    def get_document_ids_from_project_id(self, project_id):
        """
        Extracts and returns all document IDs belonging to a project.

        :param project_id: The ID of the project to query
        :return: list[str]: List of document IDs found in the project
        """
        try:
            documents = self.get_project_documents(project_id)
        except Exception:
            # optionally log the exception here
            return []
        document_ids = []
        #documents = self.get_project_documents(project_id)
        for document in documents or []:
            document_ids.append(document.document_id)
        return document_ids

    def delete_document(self, document_id):
        """
        Delete the document from the database and server. Also cleans up associated data if needed.

        :param document_id: ID of the document to delete
        :return: True if the document was deleted, False otherwise
        """

        try:
            pdf_master_id = self.document_repository.get_pdf_master_id(document_id)
        except Exception:
            return False

        self.remove_tag(document_id)
        document_data = self.document_repository.delete_document(document_id)
        self.document_repository.delete_elastic(document_id)

        if not document_data:
            print(f"Document with id {document_id} was not found")
            return False

        remote_path = self.pdf_master_repository.get_path(pdf_master_id)
        self.document_repository.delete_document(document_id)
        self.document_repository.delete_elastic(document_id)
        self.pdf_master_repository.decrement_ref_count(pdf_master_id)
        self.conversation_repository.delete_conversation_for_document(str(document_id))
        ref_count = self.pdf_master_repository.get_ref_count(pdf_master_id)

        if ref_count == 0:
            remote_dir_path = os.path.dirname(remote_path)
            delete_remote_directory(remote_dir_path)
            self.pdf_master_repository.delete_pdf_master(pdf_master_id)

        return True

    def mark_as_read(self, document_id):
        """
        Marks the document as read.

        :param document_id: ID of the document to mark as read
        :return: True if the document was marked as read, else False
        """
        return self.document_properties_repo.mark_as_read(document_id)

    def mark_as_unread(self, document_id):
        """
        Marks the document as unread.

        :param document_id: ID of the document to mark as unread
        :return: True if the document was marked as unread, else False
        """
        return self.document_properties_repo.mark_as_not_read(document_id)
    
    def add_to_favorites(self, document_id):
        """
        Adds the document to favorites.

        :param document_id: ID of the document to add
        :return: True if the document was added, else False
        """
        return self.document_properties_repo.mark_as_favorite(document_id)

    def remove_from_favorites(self, document_id):
        """
        Removes the document from favorites.

        :param document_id: ID of the document to remove
        :return: True if the document was removed, else False
        """
        return self.document_properties_repo.mark_as_not_favorite(document_id)




    def remove_tag(self, document_id):
        """
        Remove tag association from a document and clean up unused tags.

        :param document_id: ID of the document to remove tag from
        :return: bool - True if tag was successfully removed, False otherwise
        """

        try:
            document_data = self.document_repository.get_by_document_id(document_id)
        except Exception:
            return False
        if not document_data:
            return False

        tag_name = document_data.get("tag_name")
        user_id = self.document_repository.get_user_id(document_id)
        project_id = document_data.get("project_id")


        try:
            success_name = self.document_properties_repo.update_tag(document_id, None)
            success_color = self.document_properties_repo.update_tag_color(document_id, None)
        except Exception:
            return False

        success = bool(success_name and success_color)
        if not success:
            return False

        if success and tag_name:

            with mongo_connection() as db:
                count = db.documents.count_documents({"tag_name": tag_name, "project_id": project_id, "user_id": user_id})
                if count == 0:
                    db.tag_registry.delete_one({"name": tag_name, "user_id": user_id, "project_id": project_id})
                    print(f"Tag '{tag_name}' deleted from tag_registry (no longer used).")

        return success

    def get_document_tag(self, document_id):
        """
        Retrieves a document's tag from the repository.

        :param document_id: ID of the document to fetch the tag for
        :return: TagModel if tag exists, None otherwise
        """
        try:
            document_data = self.document_repository.get_by_document_id(document_id)
        except Exception:
            return None

        if not document_data:
            return None
        tag_name = document_data.get('tag_name')
        tag_color = document_data.get('tag_color')
        if tag_name and tag_color and tag_name.strip() and tag_color.strip():
            return TagModel(tag_name=tag_name, tag_color=tag_color)
        return None

    def get_project_tags(self, project_id: str, user_id: str):
        """
        Fetches tags with their colors for all documents in a project.

        :param project_id: ID of the project to fetch tags for
    :   :return: Dictionary of tag names mapped to their colors (empty if no tags found)
        """
        try:
            documents = self.get_project_documents(project_id)
        except Exception:
            return {}
        if not documents:
            return {}

        tag_set = {}

        for doc in documents:
            tag_name = doc.get_tag_name()
            if not tag_name:
                continue

            tag_data = TagRegistryRepository.get_tag(tag_name, user_id, project_id)
            tag_set[tag_name] = tag_data["color"] if tag_data else None

        return tag_set

    def filter_documents(self, project_id: str, read: bool = None, favorite: bool = None, tag: str = None):
        """
        Filters documents by read status, favorite status, and/or tag.

        :project_id ID of the project to filter documents from
        :read: If not None, filters by read status (True/False)
        :favorite: If not None, filters by favorite status (True/False)
        :tag: If not None, filters by exact tag name match
        :return: List of filtered document objects. Empty list if no matches or no documents.
        """
        try:
            all_docs = self.get_project_documents(project_id)
        except Exception:
            return []

        if not all_docs:
            return []

        filtered = []
        for doc in all_docs:
            if read is not None and doc.is_read() != read:
                continue
            if favorite is not None and doc.is_favorite() != favorite:
                continue
            if tag is not None:
                doc_tag = doc.get_tag_name()
                tag_name = doc_tag.tag_name if hasattr(doc_tag, "tag_name") else doc_tag
                if tag_name != tag:
                    continue
            filtered.append(doc)

        return filtered
    
    def get_filtered_and_sorted_documents(
        self,
        project_id: str,
        sort_field: str,
        order: str,
        read: bool = None,
        favorite: bool = None,
        tag: str = None
    ) -> list[DocumentModel]:
        """
        Retrieves documents filtered by project and optional criteria (read/favorite/tag),
        then sorts them by specified field (title/author/year/source/created_at) in given order.

        project_id: ID of project to filter documents
        sort_field: Field to sort by (title/author/year/source/created_at)
        order: Sort order ("asc" or "desc")
        read: Optional filter for read status
        favorite: Optional filter for favorite status
        tag: Optional tag to filter by
        :return: List of filtered and sorted DocumentModel objects Empty list if no documents match filters
        """
        # 1. Filter documents

        try:
            documents = self.filter_documents(project_id, read, favorite, tag)
        except Exception:
            return []

        if not documents:
            return []

        # 2. Sort documents based on sort_field
        reverse = order == "desc"
        repo = self.document_repository

        if sort_field == "title":
            documents.sort(key=lambda d: (d.name or "").lower(), reverse=reverse)
        elif sort_field == "author":
            documents.sort(key=lambda d: (repo.get_authors(d.document_id) or "").lower(), reverse=reverse)
        elif sort_field == "year":
            documents.sort(
                key=lambda d: int(repo.get_year(d.document_id)) if str(repo.get_year(d.document_id)).isdigit() else -1,
                reverse=reverse
            )
        elif sort_field == "source":
            documents.sort(key=lambda d: (repo.get_source(d.document_id) or "").lower(), reverse=reverse)
        elif sort_field == "created_at":
            documents.sort(key=lambda d: d.created_at or "", reverse=reverse)
        else:
            return documents
            #raise ValueError(f"Invalid sort field: {sort_field}")

        return documents

    def duplicate_document(self, document_id, project_id):
        """
        Duplicate a document by creating a new copy in the specified project.

        :param project_id: ID of the document to duplicate
        :param document_id: ID of the target project for the duplicated document
        :return: None
        """

        try:
            pdf_master_id = self.document_repository.get_pdf_master_id(document_id)
            pdf_name = self.document_repository.get_name(document_id)
            new_document_id = self.__create_document(document_name=pdf_name, project_id=project_id, pdf_master_id=pdf_master_id)
        except Exception:
            return None
        try:
            text = self.document_repository.get_document_text(document_id)
            self.document_repository.save_elastic(new_document_id, text)
        except Exception:
            pass
        return new_document_id

    def move_document(self, document_id, new_project_id):
        """
        Moves a document from one project to another

        :param document_id: The id of the document to move
        :param new_project_id: the id of the new project
        """

        try:
            self.document_properties_repo.set_new_project_id(document_id, new_project_id)
        except Exception:
    
            return None
    
    def search_documents(self, user_id, query):
        """
        Searches documents by title/metadata first, then by content if no matches found.

        :param user_id: User ID is to scope the search
        :param query: Search query string
        :return: List of DocumentModel objects matching the query (empty if none found)
        """
        try:
            hits = self.document_repository.search_documents(user_id, query)
        except Exception:
            return []

        if not hits:
            try:
                hits = self.document_repository.search_contents(user_id, query)
            except Exception:
                return []

        if not hits:
            return []

        document_ids = [doc['id'] for doc in hits]
        document_list = []
        for doc_id in document_ids:
            document_data = self.document_repository.get_by_document_id(doc_id)
            document_list.append(DocumentModel.from_dict(document_data))
        return document_list

    def __rename_according_ref_count(self, document_name: str, pdf_master_id: str) -> str:
        """
        Renames the document by appending reference count in parentheses if referenced.

        :param document_name: Original filename (e.g., "file.pdf")
        :param pdf_master_id: ID to check reference count in repository
        :return: Original name if ref_count=0
        """
        ref_count = self.pdf_master_repository.get_ref_count(pdf_master_id)
        if ref_count == 0:
            return document_name

        base_name, extension = os.path.splitext(document_name)
        new_name = f"{base_name}_({ref_count}){extension}"

        return new_name

    def rename_document(self, document_id, new_name):
        """
        Updates the name of a document.

        :param document_id: ID of the document to rename
        :param new_name: New name to set
        :return: True if successful, False otherwise
        """
        DocumentValidator.validate_rename(new_name)

        try:
            success = self.document_repository.update_document_name(document_id, new_name)
            return bool(success)
        except Exception:
            return False