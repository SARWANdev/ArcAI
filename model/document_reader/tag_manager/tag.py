from typing import Dict, Any
from exceptions.tag_exceptions import InvalidTagName, MissingTagColor

class Tag:
    """
    A class representing a tag with a name and color.
    """
    def __init__(self, tag_name, tag_color):
        """
        Initializes a Tag instance with a tag name and color.

        :param tag_name: The name of the tag.
        :type tag_name: str
        :param tag_color: The color of the tag in hex format.
        :type tag_color: str
        :raises InvalidTagName: If the tag name is invalid
        :raises MissingTagColor: If the tag color is missing or invalid
        """
        # Validate tag name
        if not tag_name or not isinstance(tag_name, str):
            raise InvalidTagName("Tag name must be a non-empty string")
        
        tag_name = tag_name.strip()
        if not tag_name:  # Check if empty after stripping
            raise InvalidTagName("Tag name cannot be empty or whitespace only")
        
        if len(tag_name) < InvalidTagName.MIN_NAME_LENGTH:
            raise InvalidTagName(f"Tag name must be at least {InvalidTagName.MIN_NAME_LENGTH} character long")
        
        if len(tag_name) > InvalidTagName.MAX_NAME_LENGTH:
            raise InvalidTagName(f"Tag name cannot exceed {InvalidTagName.MAX_NAME_LENGTH} characters")
        
        # Validate tag color
        if not tag_color or not isinstance(tag_color, str):
            raise MissingTagColor("Tag color must be a non-empty string")
        
        tag_color = tag_color.strip()
        if not tag_color:  # Check if empty after stripping
            raise MissingTagColor("Tag color cannot be empty or whitespace only")
        
        self.tag_name = tag_name
        self.tag_color = tag_color

    def rename_tag(self, name):
        """
        Renames the tag to a new name.

        :param name: The new name for the tag.
        :type name: str
        :raises InvalidTagName: If the new name is invalid
        """
        if not name or not isinstance(name, str):
            raise InvalidTagName("Tag name must be a non-empty string")
        
        name = name.strip()
        if len(name) < InvalidTagName.MIN_NAME_LENGTH:
            raise InvalidTagName(f"Tag name must be at least {InvalidTagName.MIN_NAME_LENGTH} character long")
        
        if len(name) > InvalidTagName.MAX_NAME_LENGTH:
            raise InvalidTagName(f"Tag name cannot exceed {InvalidTagName.MAX_NAME_LENGTH} characters")
        
        self.tag_name = name

    def set_color(self, color):
        """
        Sets a new color for the tag.

        :param color: The new color in hex format.
        :type color: str
        :raises MissingTagColor: If the color is missing or invalid
        """
        if not color or not isinstance(color, str):
            raise MissingTagColor("Tag color must be a non-empty string")
        
        color = color.strip()
        if not color:
            raise MissingTagColor("Tag color cannot be empty")
        
        self.tag_color = color

    def get_name(self):
        """
        Retrieves the name of the tag.

        :returns: The name of the tag.
        :rtype: str
        """
        return self.tag_name
    
    def get_color(self):
        """
        Retrieves the color of the tag.

        :returns: The color of the tag in hex format.
        :rtype: str
        """
        return self.tag_color
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Tag instance to a MongoDB-compatible dictionary.

        :returns: A dictionary representation of the tag.
        :rtype: Dict[str, Any]
        """
        return {
            "tag_name": self.tag_name,
            "tag_color": self.tag_color,
        }
