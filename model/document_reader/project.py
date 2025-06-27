from model.document_reader.document import Document


class Project():
    def __init__(self, project_id=None, project_name=None, user_id=None):
        self.id = project_id
        self.project_name = project_name
        self.user_id = user_id
        self.documents = []
        self.note = None

    def rename(self, name):
        self.name = name