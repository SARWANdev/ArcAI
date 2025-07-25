from typing import Dict, Any
from database.repository.date_time_utils import get_utc_zulu_timestamp


class Project():
    """
    Represents a user project.

    :param project_id: The unique identifier for the project.
    :type project_id: str or None
    :param project_name: The name of the project.
    :type project_name: str or None
    :param user_id: The ID of the user who owns the project.
    :type user_id: str or None
    :param created_at: The creation timestamp of the project.
    :type created_at: str or None
    :param updated_at: The last updated timestamp of the project.
    :type updated_at: str or None
    """
    def __init__(self, project_id=None, project_name=None, user_id=None, created_at=None, updated_at=None):
        """
        Initialize a Project instance.

        :param project_id: The unique identifier for the project.
        :type project_id: str or None
        :param project_name: The name of the project.
        :type project_name: str or None
        :param user_id: The ID of the user who owns the project.
        :type user_id: str or None
        :param created_at: The creation timestamp of the project.
        :type created_at: str or None
        :param updated_at: The last updated timestamp of the project.
        :type updated_at: str or None
        """
        self.id = project_id
        self.project_name = project_name
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.note = None

    def new_project_dict(self):
        """
        Create a dictionary representation of a new project for database insertion.

        :return: Dictionary with project fields for insertion.
        :rtype: dict
        """
        project_dict = {
            "user_id": self.user_id,
            "project_name": self.project_name,
            "note": "",
            "created_at": get_utc_zulu_timestamp(),
            "updated_at": get_utc_zulu_timestamp()
        }

        return project_dict
     
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """
        Reconstruct a Project instance from a MongoDB document.

        :param data: Dictionary from MongoDB representing a project.
        :type data: dict
        
        :return: Project instance
        :rtype: Project
        """
        return cls(
            project_id=data.get("_id") or data.get("id"),
            project_name=data.get("project_name"),
            user_id=data.get("user_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
