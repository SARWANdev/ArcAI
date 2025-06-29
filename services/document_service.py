from database.repository.document_repository import Document as DocumentRepository
from database.repository.document_properties_repository import DocumentPropertiesRepository
from model.document_reader.document import Document as DocumentModel
from model.document_reader.tag import Tag as TagModel



class DocumentService:
   
    def __init__(self):
        self.document_repository = DocumentRepository
        self.document_properties_repo = DocumentPropertiesRepository()
        self.document_repository = DocumentRepository()

    def create_document(self, project_id, name, path, note=None):
        pass

    def get_document(self, document_id):
        pass

    def get_project_documents(self, project_id):
        pass 

    def delete_document(self, document_id):
        pass

    def mark_as_read(self, document_id):
        return self.document_properties_repo.mark_as_read(document_id)

    def mark_as_unread(self, document_id):
        pass

    def download_document(self, document_id):
        pass

    def add_to_favorites(self, document_id):
        pass

    def remove_from_favorites(self, document_id):
        pass

    def add_tag(self, document_id, tag):
        pass

    def remove_tag(self, document_id):
        pass

    def get_document_tag(self, document_id):
        document_data = DocumentRepository.get_by_document_id(document_id)
        if not document_data:
            return None
        tag = TagModel(
            name = document_data.get('tag')
        )
        tag.set_color(document_data.get('tag_color'))
        return tag

    def highlight_document(self, document_id, text):
        pass

    def process_document_metadata(self, document_id):
        pass

    def duplicate_document(self, project_id, document_id):
        pass

    def extract_text_from_document(self, document_id):
        pass

    def get_text_chunks_from_document(self, document_id):
        pass

    def download_bibtex(self, document_id):
        pass

    def name_assigner(self):
        #takes the pdf information from the Bibtex and assign a name possibly athorLastName-first3Wordsof the tittle and date
        return str()
