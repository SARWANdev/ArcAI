
class MissingTagColor(Exception):
    """Tag color is missing or invalid"""
    
    def __init__(self, details: str = "Tag color is required"):
        self.details = details
        self.root_message = "Missing tag color"
        message = f"{self.root_message}: {details}"
        super().__init__(message)
