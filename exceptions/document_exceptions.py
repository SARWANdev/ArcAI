

class InvalidIdException(Exception):
    """Raised when an ID is invalid for any entity type"""
    def __init__(self, entity_type: str, details: str = "Unexpected ID violation"):
        self.entity_type = entity_type
        self.details = details
        self.root_message = f"Invalid {entity_type.lower()} id"
        message = f"{self.root_message}: {details}"
        super().__init__(message)


class InvalidServerConnectionException(Exception):
    """Raised when the server connection failed"""
    def __init__(self, details: str = "Unexpected server connection failed"):
        self.details = details
        self.root_message = "Invalid server connection"
        message = f"{self.root_message}: {details}"
        super().__init__(message)

