from database.utils.mongo_connector import mongo_connection
from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError
from exceptions.tag_exceptions import TagException, InvalidTagName, MissingTagColor

class TagRegistryRepository:
    """
    Repository class for interacting with the 'tag_registry' collection in MongoDB.
    This class provides methods to ensure indexes, retrieve, and create or verify tags.
    """

    @staticmethod
    def ensure_indexes():
        """
        Ensures that indexes are created for the 'tag_registry' collection.

        This method creates a unique index on the 'name' field to avoid duplicate tag names.

        :returns: None
        :rtype: None
        """
        with mongo_connection() as db:
            db.tag_registry.create_index([("name", ASCENDING)], unique=True)

    @staticmethod
    def get_tag(tag_name: str):
        """
        Retrieves a tag from the 'tag_registry' collection by its name.

        :param tag_name: The name of the tag to retrieve.
        :type tag_name: str

        :returns: The tag document if found, otherwise None.
        :rtype: dict | None
        """
        with mongo_connection() as db:
            return db.tag_registry.find_one({"name": tag_name})

    @staticmethod
    def create_or_verify_tag(tag_name: str, tag_color: str):
        """
        Creates a new tag or verifies an existing one in the 'tag_registry' collection.

        This method checks if the tag already exists in the collection:
        - If the tag exists with the same color, it returns the existing tag.
        - If the tag exists with a different color, it raises a `TagException`.
        - If the tag does not exist, it creates the tag and returns the newly created tag.

        :param tag_name: The name of the tag to create or verify.
        :type tag_name: str
        :param tag_color: The color associated with the tag.
        :type tag_color: str

        :returns: The tag document if it already exists or has been created.
        :rtype: dict
        
        :raises TagException: If the tag already exists with a different color.
        """
        # Validate inputs
        if not tag_name or not isinstance(tag_name, str):
            raise InvalidTagName("Tag name must be a non-empty string")
        
        tag_name = tag_name.strip()
        if len(tag_name) < InvalidTagName.MIN_NAME_LENGTH:
            raise InvalidTagName(f"Tag name must be at least {InvalidTagName.MIN_NAME_LENGTH} character long")
        
        if len(tag_name) > InvalidTagName.MAX_NAME_LENGTH:
            raise InvalidTagName(f"Tag name cannot exceed {InvalidTagName.MAX_NAME_LENGTH} characters")
        
        if not tag_color or not isinstance(tag_color, str):
            raise MissingTagColor("Tag color must be a non-empty string")
        
        tag_color = tag_color.strip()
        if not tag_color:
            raise MissingTagColor("Tag color cannot be empty")
        
        with mongo_connection() as db:
            existing = db.tag_registry.find_one({"name": tag_name})
            if existing:
                if existing.get("color") != tag_color:
                    raise TagException(f"Tag '{tag_name}' already exists with different color '{existing.get('color')}'")
                return existing
            try:
                result = db.tag_registry.insert_one({"name": tag_name, "color": tag_color})
                return {"_id": result.inserted_id, "name": tag_name, "color": tag_color}
            except DuplicateKeyError:
                # Race condition fallback
                return db.tag_registry.find_one({"name": tag_name})
