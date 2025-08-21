# exceptions/base_exceptions.py
class ArcAIException(Exception):
    """Base exception for all ArcAI application errors"""
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

class ValidationException(ArcAIException):
    """Base class for validation-related errors"""
    pass

class BusinessLogicException(ArcAIException):
    """Base class for business rule violations"""
    pass

class InfrastructureException(ArcAIException):
    """Base class for infrastructure/database/network errors"""
    pass