from exceptions.base_exceptions import BusinessLogicException
from exceptions.base_exceptions import InfrastructureException
from exceptions.base_exceptions import ValidationException

class BibTeXParseException(ValidationException):
    """Raised when a BibTeX file or entry cannot be parsed."""
    def __init__(self, details: str = "Failed to parse BibTeX entry."):
        root_message = "BibTeX parse error"
        full_message = f"{root_message}: {details}"
        super().__init__(full_message)
        self.details = details
        self.root_message = root_message


class BibTeXFieldMissingException(ValidationException):
    """Raised when a required field is missing in a BibTeX entry."""
    def __init__(self, details: str = "Required field missing in BibTeX entry."):
        root_message = "BibTeX missing field error"
        full_message = f"{root_message}: {details}"
        super().__init__(full_message)
        self.details = details
        self.root_message = root_message

class BibTeXSaveException(InfrastructureException):
    """Raised when saving a BibTeX entry or file fails."""
    def __init__(self, details: str = "Failed to save BibTeX entry or file."):
        root_message = "BibTeX save error"
        full_message = f"{root_message}: {details}"
        super().__init__(full_message)
        self.details = details
        self.root_message = root_message

class BibTeXNotFoundException(BusinessLogicException):
    """Raised when a requested BibTeX entry or file is not found."""
    def __init__(self, details: str = "BibTeX entry or file not found."):
        root_message = "BibTeX not found error"
        full_message = f"{root_message}: {details}"
        super().__init__(full_message)
        self.details = details
        self.root_message