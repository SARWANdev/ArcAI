from database.repository.user_repository import UserRepository
from database.repository.document_repository import DocumentRepository
from database.repository.conversation_repository import ConversationRepository
from exceptions.conversation_exceptions import InvalidConversationName, DuplicateConversationName, ConversationNotFoundError
from exceptions.user_exceptions import UserExceptions

class ConvesationValidator:
    
    @staticmethod
    def validate_conversation_name(self, conversation_name: str, user_id: str, exclude_conversation_id: str):
        """
        Validate conversation name according to business rules.

        :param conversation_name: The conversation name to validate.
        :type conversation_name: str
        :param user_id: The user ID to check for duplicates.
        :type user_id: str
        :param exclude_conversation_id: Conversation ID to exclude from duplicate check (for updates).
        :type exclude_conversation_id: str, optional
        :raises InvalidConversationName: If the conversation name is invalid.
        :raises DuplicateConversationName: If a conversation with the same name already exists.
        """
        
        
        try:
            self._validate_name_length(conversation_name)
            user_conversations = self.get_conversation_history(user_id)
            if user_conversations:
                for conversation in user_conversations:
                    if exclude_conversation_id and str(conversation.conversation_id) == exclude_conversation_id:
                        continue
                    if conversation.name.lower() == conversation_name.lower():
                        raise DuplicateConversationName(conversation_name)
                    
        except InvalidConversationName as e:
            return False
        except DuplicateConversationName:
            return False
                    
                
    def _validate_name_length(self, name: str):
        if not name or not name.strip():
            raise InvalidConversationName("Conversation name cannot me empty")
        
        if len(name.strip()) > InvalidConversationName.MAX_NAME_LENGTH:
            raise InvalidConversationName(f"Conversation name cannot exceed {InvalidConversationName.MAX_NAME_LENGTH} characters")
        
        if len(name.strip()) < InvalidConversationName.MIN_NAME_LENGTH:
            raise InvalidConversationName(f"Conversation name must be at least {InvalidConversationName.MIN_NAME_LENGTH} character long")
        
    def _validate_user_existence(self, user_id: str):
        pass

            
                
    