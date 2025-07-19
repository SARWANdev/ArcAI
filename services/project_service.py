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

    def sort_project_documents(self, project_id: str, sort_field: str, order: str) -> list[DocumentModel]:
        """
        Sort documents of a project by a single field.
        sort_field: one of ['title', 'author', 'year', 'source', 'created_at']
        order: 'asc' or 'desc'
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
            else:
                raise ValueError(f"Invalid sort field: {sort_field}")

        try:
            documents.sort(key=get_field_value, reverse=reverse)
        except Exception as e:
            print(f"Error while sorting documents: {e}")
            return documents  # fallback: return unsorted

        return documents


   