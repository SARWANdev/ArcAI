class BibTeXParseException(Exception):
    """Raised when a BibTeX file or entry cannot be parsed."""
    def __init__(self, details: str = "Failed to parse BibTeX entry."):
        self.details = details
        self.root_message = "BibTeX parse error"
        message = f"{self.root_message}: {details}"
        super().__init__(message)

class BibTeXSaveException(Exception):
    """Raised when saving a BibTeX entry or file fails."""
    def __init__(self, details: str = "Failed to save BibTeX entry or file."):
        self.details = details
        self.root_message = "BibTeX save error"
        message = f"{self.root_message}: {details}"
        super().__init__(message)

# BibTeX-specific NotFound exceptions removed - use NotFoundException directly