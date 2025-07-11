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

    def sort_library(self, user_id, sort_by, order='asc'):
        # Fetch all projects for the user
        library_data = self.library_repository.get_user_library(user_id)
        if not library_data:
            return []

        reverse = (order == 'desc')

        # Choose key
        if sort_by == 'name':
            key_func = lambda p: p.get('project_name', '').lower()
        elif sort_by == 'created':
            key_func = lambda p: p.get('created_at', '')
        elif sort_by == 'updated':
            key_func = lambda p: p.get('updated_at', '')
        else:
            raise ValueError(f"Invalid sort_by: {sort_by}")

        # Sort in Python
        sorted_projects = sorted(library_data, key=key_func, reverse=reverse)

        # Map to ProjectModel instances if needed
        projects_list = []
        for p in sorted_projects:
            project_model = Project.from_dict(p)
            project_model.note = p.get('note')
            projects_list.append(project_model)

        return projects_list

    def filter_library(self, filters):
        pass

    def get_item_metadata(self, item_id, item_type):
        pass
