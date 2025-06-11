
class Document:
    def __init__(self):
        self.name = self.__name_assigner() # crate a method that assign a better name according to the pattern LAst name from the author,
        self.read = False  # Private variable initialized to False
        self.tag = None
        self.metadata = None
        self.vector_store = None
        self.author = None
        self.year = None
        self.journal = None
        self.pages = None
        self.id = None

    # Optional: Getter method to access the private variable
    @property
    def read(self):
        return self.read

    def mark_document_as_read(self):
        self.read = True

    def set_name(self, name):
        self.name = name

    def set_tag(self, tag):
        self.tag = tag

    def get_tag(self):
        return self.tag
    
    def favorite(self):
        return self.favorite

    def set_favorite(self, favorite):
        self.favorite = favorite


