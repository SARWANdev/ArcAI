from exceptions.base_exceptions import ValidationException

class TagException(Exception):
    """Base exception for tag-related errors"""
    pass

class InvalidTagName(ValidationException):
    """Invalid tag name (validation error)"""
    
    # Validation constants
    MAX_NAME_LENGTH = 40
    MIN_NAME_LENGTH = 1
    
    def __init__(self, details: str = "Unspecified tag naming violation"):
        root_message = "Invalid tag name"
        super().__init__(root_message, details)
        self.details = details
        self.root_message = root_message

class MissingTagColor(ValidationException):
    """Tag color is missing or invalid"""
    
    def __init__(self, details: str = "Tag color is required"):
        root_message = "Missing tag color"
        super().__init__(root_message, details)
        self.details = details
        self.root_message = root_message
