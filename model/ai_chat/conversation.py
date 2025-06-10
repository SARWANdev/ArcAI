class Conversation:
    def __init__(self, id, name, context, vectors):
        self.id = id
        self.name = name
        self.context = context
        self.vectors = vectors

    def rename(self, name):
        self.name = name

