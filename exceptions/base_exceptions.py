# exceptions/base_exceptions.py
class ArcAIException(Exception):
    """Base exception for all ArcAI application errors"""

    def __init__(self, message: str = "An ArcAI application error occurred"):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message

class ValidationException(ArcAIException):
    """Base class for validation-related errors"""

    def __init__(self, message: str = "A validation error occurred"):
        super().__init__(message)

class BusinessLogicException(ArcAIException):
    """Base class for business rule violations"""

    def __init__(self, message: str = "A business logic error occurred"):
        super().__init__(message)

class InfrastructureException(ArcAIException):
    """Base class for infrastructure/database/network errors"""

    def __init__(self, message: str = "A infrastructure error occurred"):
        super().__init__(message)