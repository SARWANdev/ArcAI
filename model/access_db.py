from database import User, Project, Document

# Create a user
user = User("John", "Doe", "john.doe@example.com")
user_id = user.save()

# Create a project for the user
project = Project(user_id, "Website Redesign", "Redesign company website", "High priority")
project_id = project.save()

# Add a document to the project
document = Document(project_id, "Design Mockup", "/path/to/mockup.pdf", "First draft")
document_id = document.save()

# Retrieve all projects for a user
user_projects = Project.get_by_user(user_id)
print(user_projects)

# Retrieve all documents for a project
project_documents = Document.get_by_project(project_id)
print(project_documents)