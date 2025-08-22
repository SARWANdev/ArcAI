# exceptions/base_exceptions.py
class ArcAIException(Exception):
    """Base exception for all ArcAI application errors"""

    def __init__(self, message: str = "An ArcAI application error occurred"):
        super().__init__(message)
        self.message = message
        self.root_message = message

    def __str__(self) -> str:
        return self.message

class ValidationException(ArcAIException):
    """Base class for validation-related errors"""

    def __init__(self, root_message: str = "A validation error occurred", details: str = ""):
        if details:
            full_message = f"{root_message}: {details}"
        else:
            full_message = root_message
        super().__init__(full_message)
        self.root_message = root_message
        self.details = details

class BusinessLogicException(ArcAIException):
    """Base class for business rule violations"""

    def __init__(self, root_message: str = "A business logic error occurred", details: str = ""):
        if details:
            full_message = f"{root_message}: {details}"
        else:
            full_message = root_message
        super().__init__(full_message)
        self.root_message = root_message
        self.details = details

class InfrastructureException(ArcAIException):
    """Base class for infrastructure/database/network errors"""

    def __init__(self, root_message: str = "An infrastructure error occurred", details: str = ""):
        if details:
            full_message = f"{root_message}: {details}"
        else:
            full_message = root_message
        super().__init__(full_message)
        self.root_message = root_message
        self.details = details