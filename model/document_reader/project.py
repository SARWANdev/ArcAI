from model.document_reader.document import Document
from typing import Dict, Any
from datetime import datetime


class Project():
    def __init__(self, project_id=None, project_name=None, user_id=None, created_at=None, updated_at=None):
        self.id = project_id
        self.project_name = project_name
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at
        # self.documents = []
        self.note = None

    def rename(self, name):
        self.name = name

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Project instance to a MongoDB-compatible dictionary"""
        return {
            "_id": self.id,
            "project_name": self.project_name,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at or datetime.utcnow(),
            "note": self.note,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """Reconstruct a Project instance from a MongoDB document"""
        return cls(
            project_id=data.get("_id") or data.get("id"),
            project_name=data.get("project_name"),
            user_id=data.get("user_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
