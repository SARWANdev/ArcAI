from services.ai_service import AIService

class ChatController:
    def __init__(self):
        self.ai_service = AIService()

    def query(self, user_id, prompt, document_ids=None):
        pass

    def summarize(self, document_id):
        pass

    def follow_up(self, chat_id, prompt):
        pass

    def get_chat_history(self, user_id):
        pass

    def get_chat(self, chat_id):
        pass

    def rename_chat(self, chat_id, new_title):
        """
        Renames an existing chat session.
        """
        return self.ai_service.rename_chat(chat_id, new_title)

    def delete_chat(self, chat_id):
        """
        Deletes a chat session and its messages.
        """
        return self.ai_service.delete_chat(chat_id)
    
    def delete_all_chats(self, user_id):
        """
        Deletes all chat sessions for a user.
        """
        return self.ai_service.delete_all_chats(user_id)
