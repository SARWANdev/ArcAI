class Conversation:
    def __init__(self, id, name, context, vectors):
        self.id = id
        self.name = name
        self.context = context
        self.vector_store = None
        self.ai_messages = []
        self.list_of_documents = []
        self.human_messages = []

    def rename(self, name):
        self.name = name

