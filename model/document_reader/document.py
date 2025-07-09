from database.repository.date_time_utils import get_utc_zulu_timestamp


class Document:
    def __init__(self, name, project_id, pdf_master_id):
        self.name = name #self.__name_assigner() crate a method that assign a better name according to the pattern LAst name from the author,
        self.project_id = project_id
        self.pdf_master_id = pdf_master_id

    def to_dict(self):
        document_dic = {
            "name": self.name,
            "project_id": self.project_id,
            "pdf_master_id": self.pdf_master_id,
            "note": "",
            "tag": "",
            "tag_color": "",
            "read": False,
            "favorite": False,
            "created_at": get_utc_zulu_timestamp(),
            "updated_at": get_utc_zulu_timestamp(),
        }
        return document_dic



