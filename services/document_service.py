from database.repository.document_repository import DocumentDataBase as DocumentRepository
from database.repository.document_properties_repository import DocumentPropertiesRepository
from database.repository.pdf_master_repository import PdfMasterDataBase
from model.document_reader.document import Document as DocumentModel
from model.document_reader.pdf_master import PdfMaster as PdfMasterModel
from model.document_reader.tag_manager.tag import Tag as TagModel
import io

from services.upload_manager.document_upload_service import get_pdf_sha256, document_name_generator, relative_path_generator


class DocumentService:
   
    def __init__(self):
        self.document_repository = DocumentRepository 
        self.document_properties_repo = DocumentPropertiesRepository
        self.pdf_master_repository = PdfMasterDataBase

    def upload_document(self, document_path: str, user_id: str, project_id: str):

        pdf_hash = get_pdf_sha256(document_path)    # 1.  calculate the file Hash SHA-256 ++
        existing_pdf_master = self.pdf_master_repository.is_document_uploaded(pdf_hash)     # 2.  check if the SHA-256 already exists(check if that pdf is already in the database)
        # document_name = document_name_generator(document_path)
        document_name = "document dummy " # 3. generates the docuemnt name from the bibtex according to teh parameter
        new_document_instance = DocumentModel(name=document_name, project_id=project_id)    # 4. intance of the model Document
        if existing_pdf_master:
            pdf_master_id = str(existing_pdf_master.get("_id"))
            print("pdf_master_id:  if exists", pdf_master_id)
        else:
            document_path = relative_path_generator(user_id, project_id)
            new_pdf_master_instance = PdfMasterModel(path=document_path, hash=pdf_hash)
            # TODO eather update the instance or the database described in number 2
            pdf_master_id = self.pdf_master_repository.save(new_pdf_master_instance)

        new_document_id = self.document_repository.save(new_document_instance)  # saves the new document instance in the database callection documents
        self.document_repository.set_pdf_master_id(new_document_id, pdf_master_id) # set the pdf_master_id in the database for that collection
        self.pdf_master_repository.increment_ref_count(pdf_master_id) # increas by one the number of references of the pdf master

    def create_document(self, name, project_id, pdf_master_id):
        #Creates a new document in the database
        note = None #= NotebookService.create_notebook() #TODO: create new note for document's
        new_document = DocumentRepository(
            project_id = project_id,
            name = name,
            pdf_master_id = pdf_master_id,
            note = note
        )
        new_document.new_document()


    def get_document(self, document_id):
        #Gets a document from the database
        document_data = self.document_repository.get_by_document_id(document_id)
        if not document_data:
            return None
        
        document_model = DocumentModel(
            name = document_data.get('name'),
            id = document_id,
            project_id = document_data.get('project_id'),
            vector_store_path = document_data.get('vector_store_path'),
            author = document_data.get('first_author'),
            year = document_data.get('year'),
            journal = document_data.get('journal'),
            pages = document_data.get('pages')
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
        return self.document_repository.delete_document(document_id)

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

