from database.repository.conversation_repository import ConversationRepository
from model.ai_chat.conversation import Conversation as ConversationModel

class ConversationService:

    def __init__(self):
        self.conversation_repository = ConversationRepository

    def get_chat_history(self, user_id):
        conversations = ConversationRepository.get_conversations_by_user_id(user_id)
        if not conversations: 
            return None
        history = []
        for conversation in conversations:
            #TODO: wrap conversations data into model
            history.append(conversation)
        return history
    
    def get_chat(self, conversation_id):
        conversation_data = ConversationRepository.get_conversation_by_id(conversation_id)
        if not conversation_data:
            return None
        conversation_model = ConversationModel(
            id = conversation_data.get("_id"),
            vector_store = None #TODO: add vectors
        )
        #TODO: add messages into model's message list
        pass
        

    def rename_chat(self, conversation_id, new_name):
        return self.conversation_repository.update_conversation_name(conversation_id, new_name)

    def delete_chat(self, conversation_id):
        return self.conversation_repository.delete_conversation(conversation_id)

    def delete_all_chats(self, user_id):
        return self.conversation_repository.delete_all_conversations(user_id)
    
    def search_conversations(self, user_id, search):
        result = self.conversation_repository.search_conversation(user_id, search)