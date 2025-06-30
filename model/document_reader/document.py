
class Document:
    def __init__(self, name, id, project_id, vector_store_path, author, year, journal, pages):
        self.name = name #self.__name_assigner() crate a method that assign a better name according to the pattern LAst name from the author,
        self.id = id
        self.project_id = project_id
        self.read = False  # Private variable initialized to False
        self.favorite = False
        self.tag = None
        self.vector_store_path = vector_store_path
        self.author = author
        self.year = year
        self.journal = journal
        self.pages = pages

    # Optional: Getter method to access the private variable
    @property
    def read(self):
        return self.read

    def set_read(self, read):
        self.read = read

    def set_name(self, name):
        self.name = name

    def set_tag(self, tag):
        self.tag = tag

    def get_tag(self):
        return self.tag
    
    def get_favorite(self):
        return self.favorite

    def set_favorite(self, favorite):
        self.favorite = favorite


