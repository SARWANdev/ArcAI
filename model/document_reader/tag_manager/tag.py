from typing import Dict, Any

class Tag:
    def __init__(self, tag_name, tag_color):
        self.tag_name = tag_name
        self.tag_color = tag_color

    def rename_tag(self, name):
        self.tag_name = name

    def set_color(self, color):
        self.tag_color = color

    def get_name(self):
        return self.tag_name
    
    def get_color(self):
        return self.tag_color
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the Project instance to a MongoDB-compatible dictionary"""
        return {
            "tag_name": self.tag_name,
            "tag_color": self.tag_color,
        }
