from database.repository.project_repository import Project as ProjectRepository
from model.document_reader.project import Project as ProjectModel
from database.repository.library_repository import Library as LibraryRepository

class ProjectService:
    def __init__(self):
        self.project_repository = ProjectRepository
        self.library_repository = LibraryRepository

    #TODO: When thge user clicks on the "Create Project" button, a new line for a new Project will appear with an empty name,
    #TODO: and the user can fill in the name, but we should limit the name to (255)? characters.
    #TODO: We might not allow the project to have a same name as another project.
    def create_project(self, user_id, project_name):
        # 1. Create a domain object (model) for internal use
        project_model = ProjectModel(
            project_name=project_name,
            user_id=user_id,
        )

        # 2. Create a database object (repository) for persistence
        project_repo = ProjectRepository(
            user_id=user_id,
            project_name=project_name,
        )

        # 3. Insert into DB and retrieve the generated ID
        project_id = project_repo.new_project()
        project_model.id = project_id  # assign back the ID

        return project_model  # or wrap this in a DTO if needed


    def get_project(self, project_id):
        # Fetch project data from repository
        project_data = self.project_repository.get_project_by_id(project_id)
        if not project_data:
            return None
        # Map DB fields to ProjectModel
        project_model = ProjectModel(
            project_id=project_data.get('_id'),
            project_name=project_data.get('project_name'),
            user_id=project_data.get('user_id')
        )
        project_model.note = project_data.get('note')
        return project_model

    def get_user_projects(self, user_id):
        library_data = self.library_repository.get_user_library(user_id)
        if not library_data:
            return None
        projects_list = []
        for project_data in library_data:
            project_model = self.get_project(project_data.get('project_id'))
            projects_list.append(project_model)
        return projects_list

    def delete_project(self, project_id):
        return self.project_repository.delete_project(project_id)

    def rename_project(self, project_id, project_name):
        result = self.project_repository.update_name(project_id, project_name)
        return result == 1  # True if updated, False otherwise

    def download_project(self, project_id):
        pass

    def get_project_embeddings(self, project_id, document_ids=None):
        pass

    def process_project_metadata(self, project_id):
        pass

    def generate_project_summary(self, project_id):
        pass
