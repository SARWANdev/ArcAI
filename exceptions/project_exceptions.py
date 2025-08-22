from exceptions.base_exceptions import ValidationException, BusinessLogicException

class ProjectException(Exception):
    """Base exception for project-related errors"""
    pass

class ProjectNotFoundError(ProjectException):
    """Project not found in the system"""
    pass

class InvalidProjectName(ValidationException):
    """Invalid project name (validation error)"""
    
    # Validation constants
    MAX_NAME_LENGTH = 200
    MIN_NAME_LENGTH = 1
    
    def __init__(self, details: str = "Unspecified naming violation"):
        root_message = "Invalid project name"
        super().__init__(root_message, details)
        self.details = details
        self.root_message = root_message

class DuplicateProjectName(BusinessLogicException):
    """Project with same name already exists"""
    
    def __init__(self, project_name: str):
        root_message = "Project name already exists"
        details = f"Project '{project_name}' already exists in your library"
        super().__init__(root_message, details)
        self.project_name = project_name

class ProjectOperationError(ProjectException):
    """General project operation error"""
    pass
