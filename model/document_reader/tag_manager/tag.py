from typing import Dict, Any

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
        """
        self.tag_name = tag_name
        self.tag_color = tag_color

    def rename_tag(self, name):
        """
        Renames the tag to a new name.

        :param name: The new name for the tag.
        :type name: str
        """
        self.tag_name = name

    def set_color(self, color):
        """
        Sets a new color for the tag.

        :param color: The new color in hex format.
        :type color: str
        """
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
