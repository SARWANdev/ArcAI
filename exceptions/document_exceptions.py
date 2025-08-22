from exceptions.base_exceptions import ValidationException


class InvalidDocumentNaming(ValidationException):
    """Raised when a document name is invalid"""
    def __init__(self, details: str = "Unspecified naming violation"):
        root_message = "Invalid document name: "
        full_message = f"{root_message}: {details}"
        super().__init__(full_message)
        self.details = details
        self.root_message = root_message