

class InvalidUserIdException(Exception):
    """Raised when a user id is invalid"""
    def __init__(self, details: str = "Unexpected user id violation"):
        self.details = details
        self.root_message = "Invalid user id"
        message = f"{self.root_message}: {details}"
        super().__init__(message)


class InvalidProjectIdException(Exception):
    """Raised when a project id is invalid"""
    def __init__(self, details: str = "Unexpected project id violation"):
        self.details = details
        self.root_message = "Invalid project id"
        message = f"{self.root_message}: {details}"
        super().__init__(message)


class InvalidServerConnectionException(Exception):
    """Raised when the server connection failed"""
    def __init__(self, details: str = "Unexpected server connection failed"):
        self.details = details
        self.root_message = "Invalid server connection"
        message = f"{self.root_message}: {details}"
        super().__init__(message)

