
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

    #TODO: Make sure that the read and favorite functions are to a certain convention, 
    # either setters and getters or just functions
    
    def mark_read(self):
        self.read = True

    def mark_unread(self):
        self.read = False

    def is_read(self):
        return self.read

    def add_favorite(self):
        self.favorite = True

    def remove_favorite(self):
        self.favorite = False

    def is_favorite(self):
        return self.favorite



