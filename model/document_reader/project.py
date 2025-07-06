from model.document_reader.document import Document


class Project():
    def __init__(self, project_id=None, project_name=None, user_id=None, created_at=None, updated_at=None):
        self.id = project_id
        self.project_name = project_name
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.documents = []
        self.note = None

    def rename(self, name):
        self.name = name