from database.repository.project_repository import ProjectRepository
from database.repository.document_repository import DocumentRepository
from model.document_reader.project import Project as ProjectModel
from database.repository.library_repository import Library as LibraryRepository
from model.document_reader.document import Document as DocumentModel
from services.document_service import DocumentService
from services.notebook_service import NotebookService
from exceptions.base_exceptions import NotFoundException, InvalidNameError, DuplicateNameError


class ProjectService:
    """
    Service class for managing projects, including creation, retrieval, deletion, renaming, and document sorting.
    Interacts with repositories and other services to perform project-related operations.
    """
    def __init__(self):
        """
        Initialize the ProjectService with required repositories and services.
        """
        self.project_repository = ProjectRepository
        self.library_repository = LibraryRepository
        self.document_service = DocumentService()
        self.document_repository = DocumentRepository
        self.notebook_service = NotebookService()

    def create_project(self, user_id, project_name):
        """
        Create a new project for a user.

        :param user_id: The ID of the user creating the project.
        :type user_id: str
        :param project_name: The name of the new project.
        :type project_name: str
        :return: The created ProjectModel instance with assigned ID.
        :rtype: ProjectModel
        """
        # Validate project name before creation
        self._validate_project_name(project_name, user_id)
        
        project_model = ProjectModel(
            project_name=project_name,
            user_id=user_id,
        )
        project_id = self.project_repository.save(project_model)
        project_model.id = project_id
        
        # Don't call notebook service here - the note field is already set to "" in new_project_dict()
        # The notebook will be created automatically with the project
        return project_model

    def get_project(self, project_id):
        """
        Retrieve a project by its ID.

        :param project_id: The ID of the project to retrieve.
        :type project_id: str
        :return: The ProjectModel instance if found, else None.
        :rtype: ProjectModel or None
        """
        project_data = self.project_repository.get_project_by_id(project_id)
        if not project_data:
            return None
        project_model = ProjectModel.from_dict(project_data)
        project_model.note = project_data.get('note')
        return project_model

    def get_user_projects(self, user_id):
        """
        Retrieve all projects associated with a user.

        :param user_id: The ID of the user.
        :type user_id: str
        :return: List of ProjectModel instances, or None if no projects found.
        :rtype: list[ProjectModel] or None
        """
        library_data = self.library_repository.get_user_library(user_id)
        if not library_data:
            return None
        projects_list = []
        for project_data in library_data:
            project_model = self.get_project(project_data.get('_id'))
            if project_model:
                projects_list.append(project_model)
        return projects_list

    def delete_project(self, project_id):
        """
        Delete a project and all associated documents.

        :param project_id: The ID of the project to delete.
        :type project_id: str
        :return: Result of the deletion operation, or None if no documents found.
        :rtype: Any or None
        """
        documents_in_project = self.document_repository.get_documents_by_project(project_id)
        project_path = self.project_repository.get_project_by_id(project_id)  # get the path of the project
        if not documents_in_project:
            self.project_repository.delete_project(project_id)
            return None
        for document_data in documents_in_project:
            document_id = document_data.get('_id')
            self.document_service.delete_document(document_id)
            # TODO: Check if the project directory on the server is empty and, if so, delete the project directory
        return self.project_repository.delete_project(project_id)

    def rename_project(self, project_id, project_name):
        """
        Rename a project.

        :param project_id: The ID of the project to rename.
        :type project_id: str
        :param project_name: The new name for the project.
        :type project_name: str
        :return: True if updated, False otherwise.
        :rtype: bool
        """
        # Get the current project to check if it exists and get user_id
        current_project = self.get_project(project_id)
        if not current_project:
            raise NotFoundException("Project", project_id)
        
        # Validate the new project name
        self._validate_project_name(project_name, current_project.user_id, exclude_project_id=project_id)
        
        return self.project_repository.update_name(project_id, project_name)

    def sort_project_documents(self, project_id: str, sort_field: str, order: str) -> list[DocumentModel]:
        """
        Sort documents of a project by a single field.

        :param project_id: The ID of the project whose documents are to be sorted.
        :type project_id: str
        :param sort_field: The field to sort by. One of ['title', 'author', 'year', 'source', 'created_at'].
        :type sort_field: str
        :param order: The sort order, either 'asc' or 'desc'.
        :type order: str
        :return: List of sorted DocumentModel instances.
        :rtype: list[DocumentModel]
        :raises ValueError: If an invalid sort field is provided.
        """
        documents = self.document_service.get_project_documents(project_id)
        if not documents:
            return []
        reverse = order == "desc"
        repo = self.document_repository
        def get_field_value(doc: DocumentModel):
            if sort_field == "title":
                return (doc.name or "").lower()
            elif sort_field == "author":
                return (repo.get_authors(doc.document_id) or "").lower()
            elif sort_field == "year":
                year = repo.get_year(doc.document_id)
                return int(year) if str(year).isdigit() else -1
            elif sort_field == "source":
                return (repo.get_source(doc.document_id) or "").lower()
            elif sort_field == "created_at":
                return doc.created_at or ""
            raise ValueError(f"Invalid sort field: {sort_field}")
        
        documents.sort(key=get_field_value, reverse=reverse)
        return documents

    def _validate_project_name(self, project_name: str, user_id: str, exclude_project_id: str = None):
        """
        Validate project name according to business rules.
        
        :param project_name: The project name to validate.
        :type project_name: str
        :param user_id: The user ID to check for duplicates.
        :type user_id: str
        :param exclude_project_id: Project ID to exclude from duplicate check (for updates).
        :type exclude_project_id: str, optional
        :raises InvalidNameError: If the project name is invalid.
        :raises DuplicateNameError: If a project with the same name already exists.
        """
        
        # Check if project name is empty or too short
        if not project_name or not project_name.strip():
            raise InvalidNameError("Project", "Project name cannot be empty")
        
        # Check if project name is too long
        if len(project_name.strip()) > InvalidNameError.MAX_PROJECT_NAME_LENGTH:
            raise InvalidNameError("Project", f"Project name cannot exceed {InvalidNameError.MAX_PROJECT_NAME_LENGTH} characters")
        
        # Check if project name is too short
        if len(project_name.strip()) < InvalidNameError.MIN_PROJECT_NAME_LENGTH:
            raise InvalidNameError("Project", f"Project name must be at least {InvalidNameError.MIN_PROJECT_NAME_LENGTH} character long")
        
        # Check for duplicate names within the same user's library
        user_projects = self.get_user_projects(user_id)
        if user_projects:
            for project in user_projects:
                # Skip the current project when updating (to allow keeping the same name)
                if exclude_project_id and str(project.id) == exclude_project_id:
                    continue
                    
                if project.project_name.lower() == project_name.lower():
                    raise DuplicateNameError("Project", project_name)