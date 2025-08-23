from exceptions.base_exceptions import ValidationException

class NotebookException(Exception):
    """Base exception for notebook-related errors"""
    pass

class NotebookSaveException(NotebookException):
    """Exception for notebook save failures"""
    
    def __init__(self, details: str = "Unspecified notebook save error"):
        root_message = "Failed to save notebook"
        super().__init__(f"{root_message}: {details}")
        self.root_message = root_message
        self.details = details

class InvalidNoteContent(ValidationException):
    """Exception for invalid note content (validation error)"""
    
    # Only validation constant that matters
    MAX_NOTE_LENGTH = 30000  # 30KB limit for notes
    
    def __init__(self, details: str = "Unspecified content validation error"):
        root_message = "Invalid note content"
        super().__init__(root_message, details)
        self.details = details
        self.root_message = root_message

class NotebookNotFoundError(NotebookException):
    """Notebook not found in the system"""
    
    def __init__(self, notebook_type: str, entity_id: str):
        root_message = f"{notebook_type} notebook not found"
        details = f"Notebook for {notebook_type} with ID {entity_id} was not found"
        super().__init__(f"{root_message}: {details}")
        self.notebook_type = notebook_type
        self.entity_id = entity_id
        self.root_message = root_message
        self.details = details