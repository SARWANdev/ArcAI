from database.repository.library_repository import Library as LibraryRepository
from model.document_reader.library import Library as LibraryModel
from model.document_reader.project import Project

class LibraryService:
    def __init__(self):
        self.library_repository = LibraryRepository

    def get_embeddings(self, item_ids=None):
        pass

    def search_documents(self, query, filters=None):
        pass

    def sort_library(self, sort_by, sort_order='asc'):
        #Sorts library either in alphabetical, last updated or chronlogical order
        
        pass

    def filter_library(self, filters):
        pass

    def get_item_metadata(self, item_id, item_type):
        pass
