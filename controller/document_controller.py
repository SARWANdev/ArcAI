from services.document_service import DocumentService

class DocumentController:
    def __init__(self):
        self.document_service = DocumentService()

    def download_document(self, document_id):
        pass

    def download_notebook(self, notebook_id):
        pass

    def get_document_tags(self, document_id):
        pass

    def highlight_document(self, document_id, text):
        pass

    def get_document_metadata(self, document_id):
        pass

    def get_document_summary(self, document_id):
        pass

    def get_chat(self, chat_id):
        pass

    def follow_up(self, chat_id, prompt):
        pass
