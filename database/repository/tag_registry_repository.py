from database.utils.mongo_connector import mongo_connection
from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError

class TagRegistryRepository:

    @staticmethod
    def ensure_indexes():
        with mongo_connection() as db:
            db.tag_registry.create_index([("name", ASCENDING)], unique=True)

    @staticmethod
    def get_tag(tag_name: str):
        with mongo_connection() as db:
            return db.tag_registry.find_one({"name": tag_name})

    @staticmethod
    def create_or_verify_tag(tag_name: str, tag_color: str):
        with mongo_connection() as db:
            existing = db.tag_registry.find_one({"name": tag_name})
            if existing:
                if existing.get("color") != tag_color:
                    raise ValueError(f"Tag '{tag_name}' already exists with different color '{existing.get('color')}'")
                return existing
            try:
                result = db.tag_registry.insert_one({"name": tag_name, "color": tag_color})
                return {"_id": result.inserted_id, "name": tag_name, "color": tag_color}
            except DuplicateKeyError:
                # Race condition fallback
                return db.tag_registry.find_one({"name": tag_name})
