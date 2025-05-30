from Container import Container

class Project(Container):
    def _init_(self, name):
        self.name = name

    def upload_document(self):
        pass

    def download_document(self):
        pass

    def return_embedding(self):
        pass

    def delete_document(self):
        pass

    def duplicate_document(self):
        pass

    def rename(self, name):
        self.name = name