from model.document_reader.document import Document


class Project():
    def __init__(self, name):
        self.name = name
        self.documents = []
        self.id = None

    def rename(self, name):
        self.name = name