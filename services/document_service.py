import os
import tempfile
from email.mime import text
from database.repository.document_repository import DocumentDataBase as DocumentRepository
from database.repository.document_properties_repository import DocumentPropertiesRepository
from database.repository.pdf_master_repository import PdfMasterDataBase
from database.repository.tag_registry_repository import TagRegistryRepository
from database.repository.conversation_repository import ConversationRepository

from model.document_reader.document import Document as DocumentModel
from model.document_reader.pdf_master import PdfMaster as PdfMasterModel
from model.document_reader.tag_manager.tag import Tag as TagModel
from model.ai_chat.conversation import Conversation

import io
from PyPDF2 import PdfReader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from services.ai_service import AIService
from services.bibtex_service import BibTeX_Service
from services.conversation_service import ConversationService

from services.upload_manager.hash_manager import get_pdf_sha256, document_name_generator, relative_path_generator
from services.upload_manager.embeddings_manager import EmbeddingsManager
from services.upload_manager.server_conection import upload_document, delete_remote_directory, save_embeddings
from services.notebook_service import NotebookService

class DocumentService:


    def __init__(self):
        self.document_repository = DocumentRepository 
        self.document_properties_repo = DocumentPropertiesRepository
        self.conversation_repository = ConversationRepository
        self.pdf_master_repository = PdfMasterDataBase
        self.notebook_service = NotebookService()
        self.ai_service = AIService()


    def __create_document(self, document_name, project_id, pdf_master_id):
        #Creates a new document in the database
        new_name = self.__rename_according_ref_count(document_name, pdf_master_id)
        new_document_instance = DocumentModel(name = new_name, project_id = project_id, pdf_master_id = pdf_master_id)  # instance of the model Document
        new_document_id = self.document_repository.save(new_document_instance)  # saves the new document instance in the database collection documents
        #self.document_repository.set_pdf_master_id(new_document_id, pdf_master_id)  # set the pdf_master_id in the database for that collection
        self.pdf_master_repository.increment_ref_count(pdf_master_id)  # increase by one the number of references of the pdf master


        # Create an empty notebook for the document
        self.notebook_service.update_document_notebook(new_document_id, "")

        return new_document_id
    


    def __create_pdf_master(self, document_path, user_id, project_id, pdf_hash, original_name):
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

    # Endpoint Method
    def upload_file(self, file, user_id, project_id):
        original_name = file.filename
        suffix = "." + file.filename.split(".")[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
        self.upload_document(document_path = tmp_path, user_id = user_id, project_id = project_id, original_name=original_name)

        os.remove(tmp_path)



    def embeddings_storage(self, document_path, pdf_master_id):
        text_chunks = self.get_text_chunks(document=document_path)
        embeddings = self.ai_service.get_vector_store(text_chunks=text_chunks)  #
        serialized_vector_store = EmbeddingsManager.serialize_vector_store(embeddings)
        path_in_server = self.pdf_master_repository.get_path(pdf_master_id)
        paths = save_embeddings(path_in_server, serialized_vector_store[0], serialized_vector_store[1]) #save th embeddings in the server
        self.pdf_master_repository.set_remote_faiss_path(pdf_master_id, paths[0])
        self.pdf_master_repository.set_remote_pkl_path(pdf_master_id, paths[1])

        #TODO save the paths in mongo pdf_master



    def upload_document(self, document_path: str, user_id: str, project_id: str, original_name: str):

        pdf_hash = get_pdf_sha256(document_path)
        existing_pdf_master = self.pdf_master_repository.is_document_uploaded(pdf_hash, user_id)

        if existing_pdf_master:
            pdf_master_id = str(existing_pdf_master.get("_id"))

        else:
            pdf_master_id = self.__create_pdf_master(document_path, user_id, project_id, pdf_hash, original_name)
            self.embeddings_storage(document_path, pdf_master_id)

        #document_name = document_name_generator(document_path)
        #document_id = self.__create_document(os.path.basename(document_path), project_id, pdf_master_id) #TODO method the generate the name according bibtex
        document_id = self.__create_document(original_name, project_id, pdf_master_id)
        print("IMMA MAKE CONVERSATION NOW")
        ConversationService().create_document_conversation(user_id=user_id, document_id=document_id)
        print("madeit")
        #generate embeddings and vector store
        #TO run this lines of code , make sure the ollama tunel is running in the server
        text = self.get_pdf_text(document_path)

        # create a conversation for the document


        DocumentRepository.save_elastic(document_id, text)



        #text_chunks = self.get_text_chunks(document=document_path)
        #embeddings = self.ai_service.get_vector_store(text_chunks=text_chunks) #TODO save to database
        #serialized_vector_store = EmbeddingsManager.serialize_vector_store( embeddings )
        #path_in_server = self.pdf_master_repository.get_path(pdf_master_id)
        #save_embeddings(path_in_server, serialized_vector_store[0], serialized_vector_store[1])


    def get_pdf_text(self, document) -> str:
        pdf_reader = PdfReader(document) #can also take document path
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        return text
    
    def get_pdf_metadata(self, document:str):
        pdf_reader = PdfReader(document)
        metadata = pdf_reader.metadata

    def get_text_chunks(self, document)->list[str]:
        metadata = str(self.get_pdf_metadata(document=document))
        text = self.get_pdf_text(document) 
        text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
        )
    
        chunks = text_splitter.split_text(text)
        chunks.insert(0, metadata)
        return chunks




    def get_document(self, document_id):
        #Gets a document from the database
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
        if tag_name is not None and tag_color is not None:
            tag_obj = TagModel(tag_name, tag_color)
            document_model.set_tag(tag_obj)

        return document_model

    def get_project_documents(self, project_id):
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
    
    def get_document_ids_from_project_id(self, project_id):
        document_ids = []
        documents = self.get_project_documents(project_id)
        for document in documents or []:
            document_ids.append(document.document_id)
        return document_ids

    def delete_document(self, document_id):
        """
        to this method first we need to see if
        1. Check if the instance document exists ++
        2. Delete the instance document ++
        3. Decrease the reference in the pdf master ++
        4. Check how many references has the pdf master ++
        5. if the reference is 0, delete the document from the server
        6. Delete the pdf master instance ++
        7. if the project has no files , delete the directory in the server and teh instance of that project


        :param document_id:
        :return: boolean value
        """
        pdf_master_id = self.document_repository.get_pdf_master_id(document_id)
        document_data = self.document_repository.delete_document( document_id )

        if not document_data:
            print("Document with id {} was not found".format( document_id) )
            return False

        remote_path = self.pdf_master_repository.get_path( pdf_master_id )

        self.document_repository.delete_document( document_id )

        self.pdf_master_repository.decrement_ref_count( pdf_master_id )

        self.conversation_repository.delete_conversation_for_document(str(document_id))

        ref_count = self.pdf_master_repository.get_ref_count( pdf_master_id )

        if ref_count == 0:
            remote_dir_path = os.path.dirname(remote_path)
            delete_remote_directory( remote_dir_path )
            self.pdf_master_repository.delete_pdf_master( pdf_master_id )


        return True

    def mark_as_read(self, document_id):
        return self.document_properties_repo.mark_as_read(document_id)

    def mark_as_unread(self, document_id):
        return self.document_properties_repo.mark_as_not_read(document_id)
    
    def add_to_favorites(self, document_id):
        return self.document_properties_repo.mark_as_favorite(document_id)

    def remove_from_favorites(self, document_id):
        return self.document_properties_repo.mark_as_not_favorite(document_id)

    def add_tag(self, document_id, tag_name, tag_color):
        tag_obj = TagModel(tag_name, tag_color)
        tag_name = tag_obj.get_name()
        tag_color = tag_obj.get_color()


        existing_tag = TagRegistryRepository.get_tag(tag_name)
        if existing_tag:
            if existing_tag["color"] != tag_color:
                print(f"Tag with name '{tag_name}' already exists with a different color.")
                return False
           
        else:
            TagRegistryRepository.create_or_verify_tag(tag_name, tag_color)


        success_name = self.document_properties_repo.update_tag(document_id, tag_name)
        success_color = self.document_properties_repo.update_tag_color(document_id, tag_color)
        return success_name and success_color


    def remove_tag(self, document_id):
        # Step 1: Get tag_name before removal
        document_data = self.document_repository.get_by_document_id(document_id)
        if not document_data:
            return False


        tag_name = document_data.get("tag_name")


        # Step 2: Remove tag from document
        success_name = self.document_properties_repo.update_tag(document_id, None)
        success_color = self.document_properties_repo.update_tag_color(document_id, None)
        success = success_name and success_color


        # Step 3: If tag removed and tag_name existed, check if it’s unused now
        if success and tag_name:
            from database.utils.mongo_connector import mongo_connection
            with mongo_connection() as db:
                count = db.documents.count_documents({"tag_name": tag_name})
                if count == 0:
                    db.tag_registry.delete_one({"name": tag_name})
                    print(f"Tag '{tag_name}' deleted from tag_registry (no longer used).")


        return success

    def get_document_tag(self, document_id):
        document_data = self.document_repository.get_by_document_id(document_id)
        if not document_data:
            return None
        tag_name = document_data.get('tag_name')
        tag_color = document_data.get('tag_color')
        if tag_name and tag_color:
            return TagModel(name=tag_name, color=tag_color)
        return None

    def get_project_tags(self, project_id: str):
        documents = self.get_project_documents(project_id)
        if not documents:
            return {}

        tag_set = {}

        for doc in documents:
            tag_name = doc.get_tag_name()
            if not tag_name:
                continue

            tag_data = TagRegistryRepository.get_tag(tag_name)
            if tag_data:
                tag_set[tag_name] = tag_data["color"]

        return tag_set

    def filter_documents(self, project_id: str, read: bool = None, favorite: bool = None, tag: str = None):
        all_docs = self.get_project_documents(project_id)
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
        # 1. Filter documents
        documents = self.filter_documents(project_id, read, favorite, tag)
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
            raise ValueError(f"Invalid sort field: {sort_field}")

        return documents

    
    def download_document(self, document_id):
        document_data = self.document_repository.get_by_document_id(document_id)
        if not document_data:
            return None
        path = document_data.get('path')
        pdf = self.document_repository.get_pdf(document_id, path)
        return pdf

    def duplicate_document(self, document_id, project_id):
        """
        1. gets the pdf_master_id
        2. gets the name of teh document_name
        3. cretaes and new document
        :param project_id:
        :param document_id:
        :return:
        """
        pdf_master_id = self.document_repository.get_pdf_master_id(document_id)
        pdf_name = self.document_repository.get_name( document_id )
        self.__create_document(document_name = pdf_name, project_id = project_id, pdf_master_id = pdf_master_id)

    def move_document(self, document_id, new_project_id):
        """
        
        :param document_id: 
        :param new_project_id: 
        :return: 
        """

        self.document_properties_repo.set_new_project_id(document_id, new_project_id)

    def download_bibtex(self, document_id):
        # Get a document's bibtex and returns it as a buffer, with it's name
        document_data = self.document_repository.get_by_document_id(document_id)
        bibtex = document_data.get('bibtex')
        title = document_data.get('name') + '.bibtex.txt'
        if not bibtex:
            return None
        buffer = io.BytesIO()
        buffer.write(bibtex.encode('utf-8'))
        return buffer, title
    
    def search_documents(self, user_id, query):
        hits = self.document_repository.search_documents(user_id, query)
        if not hits:
            hits = self.document_repository.search_contents(user_id, query)

        if not hits:
            return []

        document_ids = [doc['id'] for doc in hits]
        document_list = []
        for id in document_ids:
            document_data = self.document_repository.get_by_document_id(id)
            document_list.append(DocumentModel.from_dict(document_data))
        return document_list

    def __rename_according_ref_count(self, document_name: str, pdf_master_id: str) -> str:
        ref_count = self.pdf_master_repository.get_ref_count(pdf_master_id)
        if ref_count == 0:
            return document_name

        base_name, extension = os.path.splitext(document_name)
        new_name = f"{base_name}_({ref_count}){extension}"

        return new_name

    def rename_document(self, document_id, new_name):
        success = self.document_repository.update_document_name(document_id, new_name)
        if success:
            print(f"Successfully updated name: {new_name}")
        else:
            print(f"Failed to update name: {new_name}")

        return success