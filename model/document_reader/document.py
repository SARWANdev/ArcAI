from typing import Optional
from database.repository.date_time_utils import get_utc_zulu_timestamp


class Document:
    """
    Represents a user document.
    """
    def __init__(self, name, project_id, pdf_master_id: Optional[str] = None, note: Optional[str] = None,
                 tag_name: Optional[str] = None, tag_color: Optional[str] = None, read: Optional[bool] = None,
                 favorite: Optional[bool] = None, created_at = None, updated_at = None, document_id: Optional[str] = None):
        """
        Initializes a Document instance with the provided parameters.

        :param name: The name of the document.
        :type name: str
        :param project_id: The ID of the project the document belongs to.
        :type project_id: str
        :param pdf_master_id: The ID of the associated PDF master (optional).
        :type pdf_master_id: str | None
        :param note: The note associated with the document (optional).
        :type note: str | None
        :param tag_name: The name of the tag associated with the document (optional).
        :type tag_name: str | None
        :param tag_color: The color of the tag associated with the document (optional).
        :type tag_color: str | None
        :param read: The read status of the document (optional).
        :type read: bool | None
        :param favorite: The favorite status of the document (optional).
        :type favorite: bool | None
        :param created_at: The timestamp when the document was created (optional).
        :type created_at: str | None
        :param updated_at: The timestamp when the document was last updated (optional).
        :type updated_at: str | None
        :param document_id: The ID of the document (optional).
        :type document_id: str | None
        """
        self.document_id = document_id
        self.name = name 
        self.project_id = project_id
        self.pdf_master_id = pdf_master_id
        self.note = note
        self.tag_name = tag_name
        self.tag_color = tag_color
        self.read = read
        self.favorite = favorite
        self.created_at = created_at
        self.updated_at = updated_at

    def new_document_dict(self):
        """
        Creates a dictionary representation of the Document instance.

        :returns: A dictionary containing the document's details.
        :rtype: dict
        """
        document_dic = {
            "name": self.name,
            "project_id": self.project_id,
            "pdf_master_id": self.pdf_master_id or "",
            "note": "",
            "tag_name": "",
            "tag_color": "",
            "read": False,
            "favorite": False,
            "created_at": get_utc_zulu_timestamp(),
            "updated_at": get_utc_zulu_timestamp(),
        }
        return document_dic

    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a Document instance from a dictionary.

        :param data: The dictionary containing the document's data.
        :type data: dict
        
        :returns: A Document instance populated with the provided data.
        :rtype: Document
        """
        return cls(
            name=data.get("name"),
            project_id=data.get("project_id"),
            pdf_master_id=data.get("pdf_master_id"),
            note=data.get("note"),
            tag_name=data.get("tag_name"),
            tag_color=data.get("tag_color"),
            read=data.get("read"),
            favorite=data.get("favorite"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            document_id=str(data.get("_id"))
        )

    #TODO: Make sure that the read and favorite functions are to a certain convention, 
    # either setters and getters or just functions
    
    def mark_read(self):
        """
        Marks the document as read.

        """
        self.read = True

    def mark_unread(self):
        """
        Marks the document as unread.

        """
        self.read = False

    def is_read(self):
        """
        Marks the document as read.

        """
        return self.read

    def add_favorite(self):
        """
        Adds the document as favorite.

        """
        self.favorite = True

    def remove_favorite(self):
        """
        Removes the document from favorite.

        """
        self.favorite = False

    def is_favorite(self):
        """
        Checks if the document is marked as favorite.

        :returns: True if the document is favorite, otherwise False.
        :rtype: bool
        """
        return self.favorite

    def set_tag(self, tag_obj):
        """
        Sets the tag for the document.

        :param tag_obj: The tag object containing the tag name and color.
        :type tag_obj: TagModel
        """
        self.tag_name = tag_obj.get_name()
        self.tag_color = tag_obj.get_color()

    def get_tag_name(self):
        """
        Gets the name of the tag associated with the document.

        :returns: The tag name.
        :rtype: str
        """
        return self.tag_name

    def get_pdf_master(self):
        """
        Retrieves the PDF master ID associated with the document.

        :returns: The PDF master ID.
        :rtype: str
        """
        return self.pdf_master_id



