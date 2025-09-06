# Tag-specific naming exceptions removed - use InvalidNameError directly

class MissingTagColor(Exception):
    """Tag color is missing or invalid"""
    
    def __init__(self, details: str = "Tag color is required"):
        self.details = details
        self.root_message = "Missing tag color"
        message = f"{self.root_message}: {details}"
        super().__init__(message)

class DuplicateTagColor(Exception):
    """Tag already exists with a different color"""
    
    def __init__(self, tag_name: str, existing_color: str, new_color: str):
        self.tag_name = tag_name
        self.existing_color = existing_color
        self.new_color = new_color
        self.root_message = "Tag color conflict"
        self.details = f"Tag '{tag_name}' already exists with different color '{existing_color}'"
        message = f"{self.root_message}: {self.details}"
        super().__init__(message)
