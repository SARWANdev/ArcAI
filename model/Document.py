
class Document:
    def __init__(self):
        self.name = self.__name_assigner() # crate a method that assign a better name according to the pattern LAst name from the author,
        self.__is_document_read = False  # Private variable initialized to False
        self.tag = None
        self.metadata = None

    # Optional: Getter method to access the private variable
    @property
    def is_document_read(self):
        return self.__is_document_read

    def mark_document_as_read(self):
        self.__is_document_read = True

    def __name_assigner(self):
        #takes the pdf information from the Bibtex and assign a name possibly athorLastName-first3Wordsof the tittle and date
        return str()

    def rename_document(new_name):
        name = new_name

    def add_tag(self, tag):
        self.tag = tag

    def remove_tag(self):
        self.tag = None

    def get_tag(self):
        return self.tag

    def highlight(self):
        pass
