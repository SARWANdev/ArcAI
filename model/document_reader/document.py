
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

    # Optional: Getter method to access the private variable
    @property
    def read(self):
        return self.read
    

    def mark_document_as_read(self):
        self.read = True

    def __name_assigner(self):
        #takes the pdf information from the Bibtex and assign a name possibly athorLastName-first3Wordsof the tittle and date
        return str()

    def rename_document(self, name):
        self.name = name

    def add_tag(self, tag):
        self.tag = tag

    def remove_tag(self):
        self.tag = None

    def get_tag(self):
        return self.tag

    def highlight(self):
        pass
