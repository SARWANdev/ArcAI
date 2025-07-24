from database.repository.library_repository import Library as LibraryRepository
from model.document_reader.project import Project

class LibraryService:
    """
    Library service module for handling library-related business logic.

    Provides methods to sort and retrieve user library projects.
    """
    def __init__(self):
        """
        Initialize the LibraryService with a library repository instance.
        """
        self.library_repository = LibraryRepository

    def sort_library(self, user_id, sort_by, order='asc'):
        """
        Sort the user's library projects by a specified field and order.

        :param user_id: The unique identifier of the user whose library is to be sorted.
        :type user_id: str or ObjectId
        :param sort_by: The field to sort by ('name', 'created', or 'updated').
        :type sort_by: str
        :param order: The sort order, either 'asc' for ascending or 'desc' for descending. Defaults to 'asc'.
        :type order: str, optional
        :return: A list of Project instances sorted as specified.
        :rtype: list[Project]
        :raises ValueError: If sort_by is not a valid field.
        """
        library_data = self.library_repository.get_user_library(user_id)
        if not library_data:
            return []

        reverse = (order == 'desc')

        if sort_by == 'name':
            key_func = lambda p: p.get('project_name', '').lower()
        elif sort_by == 'created':
            key_func = lambda p: p.get('created_at', '')
        elif sort_by == 'updated':
            key_func = lambda p: p.get('updated_at', '')
        else:
            raise ValueError(f"Invalid sort_by: {sort_by}")

        sorted_projects = sorted(library_data, key=key_func, reverse=reverse)

        projects_list = []
        for project_dict in sorted_projects:
            project_model = Project.from_dict(project_dict)
            project_model.note = project_dict.get('note')
            projects_list.append(project_model)

        return projects_list

