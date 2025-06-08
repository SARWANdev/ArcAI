# from database.repository.conversation_repository import Chat as ConversationRepository
# from model.chat import Chat as ConversationModel

class AIService:
    def __init__(self):
        self.conversation_repository = ConversationRepository

    def query(self, user_id, prompt, document_ids=None):
        # TODO: Send prompt to LLM (e.g., GPT/Claude), possibly with doc context
        pass

    def summarize(self, document_id):
        # TODO: Extract document text and return a summary
        pass

    def follow_up(self, chat_id, prompt):
        # TODO: Continue previous chat session with new prompt
        pass

    def get_chat_history(self, user_id):
        # TODO: Fetch all chat sessions for the user
        pass

    def rename_chat(self, chat_id, new_title):
        # TODO: Rename the chat in DB
        pass

    def delete_chat(self, chat_id):
        # TODO: Hard-delete or soft-delete the chat session
        pass
