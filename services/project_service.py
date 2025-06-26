from database.repository.project_repository import Project as ProjectRepository
from model.document_reader.project import Project as ProjectModel

class ProjectService:
    def __init__(self):
        self.project_repository = ProjectRepository

    #TODO: When the user clicks on the "Create Project" button, a new line for a new Project will appear with an empty name,
    #TODO: and the user can fill in the name, but we should limit the name to (255)? characters.
    #TODO: We might not allow the project to have a same name as another project.
    def create_project(self, user_id, name):
        # 1. Create a domain object (model) for internal use
        project_model = ProjectModel(
            name=name,
            user_id=user_id,
        )

        # 2. Create a database object (repository) for persistence
        project_repo = ProjectRepository(
            user_id=user_id,
            name=name,
        )

        # 3. Insert into DB and retrieve the generated ID
        project_id = project_repo.new_project()
        project_model.id = project_id  # assign back the ID

        return project_model  # or wrap this in a DTO if needed


    def get_project(self, project_id):
        # Fetch project data from repository
        project_data = self.project_repository.get_by_id(project_id)
        if not project_data:
            return None
        # Map DB fields to ProjectModel
        project_model = ProjectModel(
            project_id=project_data.get('project_id'),
            name=project_data.get('name'),
            user_id=project_data.get('user_id')
        )
        project_model.note = project_data.get('note')
        return project_model

    def get_user_projects(self, user_id):
        pass

    def delete_project(self, project_id):
        pass

    def rename_project(self, project_id, name):
        result = self.project_repository.update_name(project_id, name)
        return result == 1  # True if updated, False otherwise

    def download_project(self, project_id):
        pass

    def get_project_embeddings(self, project_id, document_ids=None):
        pass

    def process_project_metadata(self, project_id):
        pass

    def generate_project_summary(self, project_id):
        pass
