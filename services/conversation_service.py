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
            user_id = conversation_data.get("user_id"),
            name = conversation_data.get("name"),
            messages = conversation_data.get("messages"),
            list_of_documents = conversation_data.get("list_of_documents"),
            vector_store = conversation_data.get("vector_store"),
            created_at = conversation_data.get("created_at"),
            updated_at = conversation_data.get("updated_at")
        )
        return conversation_model
        
    
    def rename_chat(self, conversation_id, new_name):
        return self.conversation_repository.update_conversation_name(conversation_id, new_name)

    def delete_chat(self, conversation_id):
        return self.conversation_repository.delete_conversation(conversation_id)

    def delete_all_chats(self, user_id):
        return self.conversation_repository.delete_all_conversations(user_id)
    
    def search_conversations(self, user_id, search):
        result = self.conversation_repository.search_conversation(user_id, search)
        return result