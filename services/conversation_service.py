from database.repository.conversation_repository import ConversationRepository
from model.ai_chat.conversation import Conversation as ConversationModel
from bson import ObjectId


class ConversationService:

    def __init__(self):
        self.conversation_repository = ConversationRepository

    def get_chat_history(self, user_id):
        conversations = ConversationRepository.get_history(user_id)
        if not conversations: 
            return None
        history = []
        for conversation in conversations:
            conversation_data = ConversationRepository.get_conversation_by_id(conversation.get("_id"))
            conversation_model = ConversationModel(
            conversation_id= conversation_data.get("_id"),
            user_id = conversation_data.get("user_id"),
            name = conversation_data.get("name"),
            messages = conversation_data.get("messages"),
            vector_store = conversation_data.get("vector_store"),
            created_at = conversation_data.get("created_at"),
            updated_at = conversation_data.get("updated_at")
            )
            history.append(conversation_model)
        return history
    
    def get_chat(self, conversation_id):
        conversation_data = ConversationRepository.get_conversation_by_id(conversation_id)
        if not conversation_data:
            return None
        conversation_model = ConversationModel(
            conversation_id= conversation_data.get("_id"),
            user_id = conversation_data.get("user_id"),
            name = conversation_data.get("name"),
            messages = conversation_data.get("messages"),
            vector_store = conversation_data.get("vector_store"),
            created_at = conversation_data.get("created_at"),
            updated_at = conversation_data.get("updated_at")
        )
        return conversation_model
        
    def add_to_history(self, conversation_id):
        return ConversationRepository.add_to_history(conversation_id)
    
    def rename_chat(self, conversation_id, new_name):
        return ConversationRepository.update_conversation_name(conversation_id, new_name)

    def delete_chat(self, conversation_id):
        return ConversationRepository.delete_conversation(conversation_id)

    def delete_all_chats(self, user_id):
        return ConversationRepository.delete_all_conversations(user_id)
    
    def search_conversations(self, user_id, search):
        result = ConversationRepository.search_conversation(user_id, search)
        return result