from services.document_service import DocumentService
from services.notebook_service import NotebookService
from services.ai_service import AIService

class DocumentController:
    def __init__(self):
        self.document_service = DocumentService()
        self.notebook_service = NotebookService()
        self.ai_service = AIService()

    def download_document(self, document_id):
        pass

    def download_notebook(self, notebook_id):
        pass

    def edit_notebook(self, notebook_id, prompt):
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
