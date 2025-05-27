from abc import ABC, abstractmethod
class Container(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def upload_document(self):
        pass

    @abstractmethod
    def download_document(self):
        pass

    @abstractmethod
    def return_embedding(self):
        pass  

    @abstractmethod
    def delete_document(self):
        pass
    @abstractmethod
    def duplicate_document(self):
        pass

    @abstractmethod
    def rename(self, name):
        self.name = name

    @abstractmethod
    def download():
        pass