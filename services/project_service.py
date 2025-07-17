from database.repository.project_repository import Project as ProjectRepository
from database.repository.document_repository import DocumentDataBase as DocumentRepository
from model.document_reader.project import Project as ProjectModel
from database.repository.library_repository import Library as LibraryRepository
from model.document_reader.document import Document as DocumentModel
from services.document_service import DocumentService
from services.notebook_service import NotebookService

class ProjectService:
    def __init__(self):
        self.project_repository = ProjectRepository
        self.library_repository = LibraryRepository
        self.document_service = DocumentService()
        self.document_repository = DocumentRepository
        self.notebook_service = NotebookService()

    #TODO: When thge user clicks on the "Create Project" button, a new line for a new Project will appear with an empty name,
    #TODO: and the user can fill in the name, but we should limit the name to (255)? characters.
    #TODO: We might not allow the project to have a same name as another project.
    def create_project(self, user_id, project_name):
        # 1. Create a domain object (model) for internal use
        project_model = ProjectModel(
            project_name=project_name,
            user_id=user_id,
            note=""
        )

        # 2. 2. Save to DB using static repository
        project_id = self.project_repository.new_project(user_id, project_name, note="")
        project_model.id = project_id  # assign back the ID
        self.notebook_service.update_project_notebook(project_id, "")

        return project_model  # or wrap this in a DTO if needed


    def get_project(self, project_id):
        # Fetch project data from repository
        project_data = self.project_repository.get_project_by_id(project_id)
        if not project_data:
            return None
        # Map DB fields to ProjectModel
        project_model = ProjectModel.from_dict(project_data)
        project_model.note = project_data.get('note')
        return project_model

    def get_user_projects(self, user_id):
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
        documents_in_project = self.document_repository.get_documents_by_project( project_id )
        project_path = self.project_repository.get_project_by_id(project_id) #get the path of the project
        if not documents_in_project:
            return None

        for document_data in documents_in_project:
            document_id = document_data.get('_id')
            document_path = self.document_repository.get_path(document_id)
            self.document_service.delete_document(document_id)
            #TODO check if the directory of project in the server is empty and if that's the case , delete the project directory




        return self.project_repository.delete_project(project_id)

    def rename_project(self, project_id, project_name):
        result = self.project_repository.update_name(project_id, project_name)
        return result == 1  # True if updated, False otherwise

    def download_project(self, project_id):
        pass

    def sort_project_documents(self, project_id: str, sort_criteria: list[tuple[str, str]]) -> list[DocumentModel]:
        """
        Sort documents of a project by multiple criteria.
        Each entry in sort_criteria is a tuple: (field_name, order)
        e.g., [('author', 'asc'), ('year', 'desc'), ('title', 'asc')]
        """
        documents = self.document_service.get_project_documents(project_id)
        if not documents:
            return []

        valid_fields = {
            "title": lambda d: getattr(d, 'name', '').lower() if getattr(d, 'name', None) else "",
            "author": lambda d: getattr(d, 'author', '').lower() if getattr(d, 'author', None) else "",
            "year": lambda d: getattr(d, 'year', None) if getattr(d, 'year', None) is not None else -1,
            "source": lambda d: getattr(d, 'source', '').lower() if getattr(d, 'source', None) else "",
            "created_at": lambda d: getattr(d, 'created_at', '') if getattr(d, 'created_at', None) else ""
        }


        for field, order in reversed(sort_criteria):
            if field not in valid_fields:
                raise ValueError(f"Invalid sort field: {field}")
            reverse = (order == "desc")
            documents.sort(key=valid_fields[field], reverse=reverse)

        return documents


    #SHRAWAN
    def get_project_embeddings(self, project_id, document_ids=None):
        pass

    #SHRAWAN
    def generate_project_summary(self, project_id):
        pass
