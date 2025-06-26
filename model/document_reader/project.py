from model.document_reader.document import Document


class Project():
    def __init__(self, project_id=None, name=None, user_id=None):
        self.id = project_id
        self.name = name
        self.user_id = user_id
        self.documents = []
        self.note = None

    def rename(self, name):
        self.name = name