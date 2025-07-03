from database.repository.document_repository import Document as DocumentRepository
from database.repository.document_properties_repository import DocumentPropertiesRepository
from model.document_reader.document import Document as DocumentModel
from model.document_reader.tag import Tag as TagModel
import io



class DocumentService:
   
    def __init__(self):
        self.document_repository = DocumentRepository
        self.document_properties_repo = DocumentPropertiesRepository()
        self.document_repository = DocumentRepository()

    def create_document(self, name, project_id, path, vector_store_path, author, year, journal, pages, bibtex):
        #Creates a new document in the database
        note = None #= NotebookService.create_notebook() #TODO: create new note for document's
        new_document = DocumentRepository(project_id, name, path, vector_store_path, author, year, journal, pages, bibtex)
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
        document_model.set_tag = document_data.get('tag')
        document_model.set_read = document_data.get('read')
        document_model.set_favorite = document_data.get('favorite')
        return document_model

    def get_project_documents(self, project_id):
        documents_data = self.document_repository.get_documents_by_project(project_id) 
        if not documents_data:
            return None
        documents_list = []
        for document_data in documents_data:
            document_model = self.get_document(document_data.get('_id'))
            documents_list.append(document_model)
        return documents_list

    def delete_document(self, document_id):
        return self.document_repository.delete_document(document_id)

    def mark_as_read(self, document_id):
        return self.document_properties_repo.mark_as_read(document_id)

    def mark_as_unread(self, document_id):
        return self.document_properties_repo.mark_as_not_read(document_id)

    def download_document(self, document_id):
        document_data = self.document_repository.get_by_document_id(document_id)
        if not document_data:
            return None
        path = document_data.get('path')
        pdf = self.document_repository.get_pdf(document_id, path)
        return pdf

    def add_to_favorites(self, document_id):
        return self.document_properties_repo.mark_as_favorite(document_id)

    def remove_from_favorites(self, document_id):
        return self.document_properties_repo.mark_as_not_favorite(document_id)

    def add_tag(self, document_id, tag, color):
        return self.document_properties_repo.update_tag(document_id, tag, color)

    def remove_tag(self, document_id):
        return self.document_properties_repo.update_tag(document_id, None) & self.document_properties_repo.update_tag_color(document_id, None)

    def get_document_tag(self, document_id):
        document_data = self.document_repository.get_by_document_id(document_id)
        if not document_data:
            return None
        tag = TagModel(
            name = document_data.get('tag'),
            color = document_data.get('tag_color')
        )
        return tag

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
