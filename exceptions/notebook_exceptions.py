class NotebookSaveException(Exception):
    """Exception for notebook save failures"""
    
    def __init__(self, details: str = "Unspecified notebook save error"):
        self.root_message = "Failed to save notebook"
        self.details = details
        message = f"{self.root_message}: {details}"
        super().__init__(message)

class InvalidNoteContent(Exception):
    """Exception for invalid note content (validation error)"""
    
    # Only validation constant that matters
    MAX_NOTE_LENGTH = 30000  # 30KB limit for notes
    
    def __init__(self, details: str = "Unspecified content validation error"):
        self.details = details
        self.root_message = "Invalid note content"
        message = f"{self.root_message}: {details}"
        super().__init__(message)

# Notebook-specific NotFound exceptions removed - use NotFoundException directly