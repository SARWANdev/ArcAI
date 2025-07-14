import os
from email.mime import text
from database.repository.document_repository import DocumentDataBase as DocumentRepository
from database.repository.document_properties_repository import DocumentPropertiesRepository
from database.repository.pdf_master_repository import PdfMasterDataBase
from model.document_reader.document import Document as DocumentModel
from model.document_reader.pdf_master import PdfMaster as PdfMasterModel
from model.document_reader.tag_manager.tag import Tag as TagModel
import io
from PyPDF2 import PdfReader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from services.ai_service import AIService
from services.bibtex_service import title, BibTeX_Service

from services.upload_manager.document_upload_service import get_pdf_sha256, document_name_generator, relative_path_generator
from services.upload_manager.server_conection import upload_document, delete_remote_directory


class DocumentService:


    def __init__(self):
        self.document_repository = DocumentRepository 
        self.document_properties_repo = DocumentPropertiesRepository
        self.pdf_master_repository = PdfMasterDataBase


    def __create_document(self, document_name, project_id, pdf_master_id):
        #Creates a new document in the database
        new_document_instance = DocumentModel(name=document_name, project_id=project_id)  # instance of the model Document
        new_document_id = self.document_repository.save(new_document_instance)  # saves the new document instance in the database collection documents
        self.document_repository.set_pdf_master_id(new_document_id, pdf_master_id)  # set the pdf_master_id in the database for that collection
        self.pdf_master_repository.increment_ref_count(pdf_master_id)  # increase by one the number of references of the pdf master

    def __create_pdf_master(self, document_path, user_id, project_id, pdf_hash):
        relative_path = relative_path_generator(user_id, project_id)
        title = os.path.basename(document_path)
        bibtex_instance = BibTeX_Service(title)
        pdf_path_in_server = upload_document(local_path = document_path, relative_path = relative_path, pdf_hash = pdf_hash)
        new_pdf_master_instance = PdfMasterModel(path = pdf_path_in_server, pdf_hash = pdf_hash, user_id = user_id,
                                                 year = bibtex_instance.get_year(), source = bibtex_instance.get_source(),
                                                 authors = bibtex_instance.get_authors())
        # TODO eather update the instance or the database described with the bibtex


           # string type
        pdf_master_id = self.pdf_master_repository.save(new_pdf_master_instance)
        return pdf_master_id

    def file_to_path(self, file, user_id, project_id):
        pass




    def upload_document(self, document_path: str, user_id: str, project_id: str):

        pdf_hash = get_pdf_sha256(document_path)
        existing_pdf_master = self.pdf_master_repository.is_document_uploaded(pdf_hash, user_id)

        if existing_pdf_master:
            pdf_master_id = str(existing_pdf_master.get("_id"))
        else:
            pdf_master_id = self.__create_pdf_master(document_path, user_id, project_id, pdf_hash)

        #document_name = document_name_generator(document_path)
        self.__create_document(os.path.basename(document_path), project_id, pdf_master_id) #TODO method the generate the name according bibtex

        #generate embeddings and vector store

        text_chunks = self.__get_text_chunks(document_path=document_path)       
        ai_service = AIService()
        embeddings = ai_service.get_vector_store(text_chunks=text_chunks, embedding_path=document_path+".FAISS") #TODO save to database


    def __get_pdf_text(self, document_path:str) -> str:
        pdf_reader = PdfReader(document_path)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        return text
    
    def get_pdf_metadata(self, document_path:str):
        pdf_reader = PdfReader(document_path)
        metadata = pdf_reader.metadata

    def __get_text_chunks(self, document_path:str)->list[str]:
        metadata = str(self.get_pdf_metadata(document_path=document_path))
        text = self.__get_pdf_text(document_path) 
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
            id=document_id,
            name=document_data.get('name'),
            project_id=document_data.get('project_id'),
            pdf_master_id=document_data.get('pdf_master_id'),
            note=document_data.get('note'),
            tag=document_data.get('tag'),
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

        tag_name = document_data.get('tag')
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

        ref_count = self.pdf_master_repository.get_ref_count( pdf_master_id )

        if ref_count == 0:

            delete_remote_directory( remote_path )
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
        success_name = self.document_properties_repo.update_tag(document_id, tag_name)
        success_color = self.document_properties_repo.update_tag_color(document_id, tag_color)
        return success_name and success_color

    def remove_tag(self, document_id):
        return self.document_properties_repo.update_tag(document_id, None) & self.document_properties_repo.update_tag_color(document_id, None)

    def get_document_tag(self, document_id):
        document_data = self.document_repository.get_by_document_id(document_id)
        if not document_data:
            return None
        tag_name = document_data.get('tag')
        tag_color = document_data.get('tag_color')
        if tag_name and tag_color:
            return TagModel(name=tag_name, color=tag_color)
        return None
    
    def download_document(self, document_id):
        document_data = self.document_repository.get_by_document_id(document_id)
        if not document_data:
            return None
        path = document_data.get('path')
        pdf = self.document_repository.get_pdf(document_id, path)
        return pdf

    def highlight_document(self, document_id, text):
        pass

    def process_document_metadata(self, document_id):
        pass

    def duplicate_document(self, document_id):
        #TODO: duplicate the document in the database
        document_data = self.document_repository.get_by_document_id(document_id)
        if not document_data:
            return None

    def extract_text_from_document(self, document_id):
        pass

    def get_text_chunks_from_document(self, document_id):
        pass

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
        

    def name_assigner(self):
        #takes the pdf information from the Bibtex and assigns a name, possibly athorLastName-first3Wordsof the title and date
        return str()
    
    def search_documents(self, prefix):
        found_documents = self.document_repository.search(prefix)
        documents_list = []
        for document_data in found_documents:
            doc_id = document_data.get('_id')
            document_model = self.get_document(doc_id)
            if document_model:
                documents_list.append(document_model)
        return documents_list

