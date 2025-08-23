from exceptions.base_exceptions import ValidationException, BusinessLogicException, InfrastructureException


class InvalidDocumentNamingException(ValidationException):
    """Raised when a document name is invalid"""
    def __init__(self, details: str = "Unspecified naming violation"):
        root_message = "Invalid document name: "
        full_message = f"{root_message}: {details}"
        super().__init__(full_message)
        self.details = details
        self.root_message = root_message

class InvalidUserIdException(BusinessLogicException):
    """Raised when a document name is invalid"""
    def __init__(self, details: str = "Unexpected user id violation"):
        root_message = "Invalid user id: "
        full_message = f"{root_message}: {details}"
        super().__init__(full_message)
        self.details = details
        self.root_message = root_message

class InvalidProjectIdException(BusinessLogicException):
    """Raised when a document name is invalid"""
    def __init__(self, details: str = "Unexpected project id violation"):
        root_message = "Invalid project id: "
        full_message = f"{root_message}: {details}"
        super().__init__(full_message)
        self.details = details
        self.root_message = root_message

class InvalidServerConversation(InfrastructureException):
    """Raised when the server connection failed"""

    def __init__(self, details: str = "Unexpected server connection failed"):
        root_message = "Invalid server connection: "
        full_message = f"{root_message}: {details}"
        super().__init__(full_message)
        self.details = details
        self.root_message = root_message

