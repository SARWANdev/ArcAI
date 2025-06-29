class History:
    def __init__(self, conversations):
        self.conversations = list()

    def add_conversation(self, conversation):
        self.conversations.append(conversation)
    
    def delete_conversation(self, conversation):
        self.conversations.remove(conversation)
