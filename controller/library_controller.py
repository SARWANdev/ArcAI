from services.library_service import LibraryService

class LibraryController:
    def __init__(self):
        self.library_service = LibraryService()

    def move_item(self, item_id, item_type, destination_id):
        pass

    def duplicate_item(self, item_id, item_type):
        pass

    def download_item(self, item_id, item_type):
        pass

    def get_embeddings(self, item_ids=None):
        pass

    def search_documents(self, query, filters=None):
        pass

    def sort_library(self, sort_by, sort_order='asc'):
        pass

    def get_library_structure(self):
        pass

    def filter_library(self, filters):
        pass

    def get_item_metadata(self, item_id, item_type):
        pass
