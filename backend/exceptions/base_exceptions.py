# exceptions/base_exceptions.py

class NotFoundException(Exception):
    """Generic exception for when an entity is not found"""
    
    def __init__(self, entity_type: str, entity_id: str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        message = f"{entity_type} with ID '{entity_id}' not found"
        super().__init__(message)
        self.message = message
        self.root_message = f"{entity_type} not found"
        self.details = f"{entity_type} with ID '{entity_id}' does not exist"


class InvalidNameException(Exception):
    """Generic exception for invalid names with validation constants"""

    # Validation constants for different entity types
    MAX_CONVERSATION_NAME_LENGTH = 100
    MIN_CONVERSATION_NAME_LENGTH = 1

    MAX_PROJECT_NAME_LENGTH = 80
    MIN_PROJECT_NAME_LENGTH = 1

    MAX_DOCUMENT_NAME_LENGTH = 2000
    MIN_DOCUMENT_NAME_LENGTH = 1

    MAX_TAG_NAME_LENGTH = 40
    MIN_TAG_NAME_LENGTH = 1

    def __init__(self, entity_type: str, details: str = "Unspecified naming violation"):
        self.entity_type = entity_type
        self.details = details
        self.root_message = f"Invalid {entity_type.lower()} name"
        message = f"{self.root_message}: {details}"
        super().__init__(message)


class DuplicateNameException(Exception):
    """Generic exception for duplicate names"""

    def __init__(self, entity_type: str, entity_name: str):
        self.entity_type = entity_type
        self.entity_name = entity_name
        self.root_message = f"{entity_type} name already exists"
        self.details = f"{entity_type} '{entity_name}' already exists in your library"
        message = f"{self.root_message}: {self.details}"
        super().__init__(message)