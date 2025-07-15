from typing import Optional

from database.repository.date_time_utils import get_utc_zulu_timestamp


class Document:
    def __init__(self, name, project_id, pdf_master_id: Optional[str] = None, note: Optional[str] = None,
                 tag_name: Optional[str] = None, tag_color: Optional[str] = None, read: Optional[bool] = None,
                 favorite: Optional[bool] = None, created_at = None, updated_at = None, document_id: Optional[str] = None):
        self.document_id = document_id
        self.name = name #self.__name_assigner() crate a method that assign a better name according to the pattern Last name from the author,
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
        document_dic = {
            "name": self.name,
            "project_id": self.project_id,
            "pdf_master_id": "",
            "note": "",
            "tag_name": "",
            "tag_color": "",
            "read": False,
            "favorite": False,
            "created_at": get_utc_zulu_timestamp(),
            "updated_at": get_utc_zulu_timestamp(),
        }
        return document_dic


    #TODO: Make sure that the read and favorite functions are to a certain convention, 
    # either setters and getters or just functions
    
    def mark_read(self):
        self.read = True

    def mark_unread(self):
        self.read = False

    def is_read(self):
        return self.read

    def add_favorite(self):
        self.favorite = True

    def remove_favorite(self):
        self.favorite = False

    def is_favorite(self):
        return self.favorite

    def set_tag(self, tag_obj):
        self.tag_name = tag_obj.get_name()
        self.tag_color = tag_obj.get_color()

    def get_tag(self):
        return self.tag_name



