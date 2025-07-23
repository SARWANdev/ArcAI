"""
Service layer for managing conversations.
"""
from typing import List, Optional, Any
from database.repository.conversation_repository import ConversationRepository
from model.ai_chat.conversation import Conversation as ConversationModel
from bson import ObjectId
from database.repository.date_time_utils import get_utc_zulu_timestamp


class ConversationService:
    """
    Service for handling conversation-related operations.
    """

    def __init__(self):
        self.conversation_repository = ConversationRepository

    def create_conversation(
        self,
        user_id: Any,
        document_ids: List[Any],
        project_ids: Optional[List[Any]] = None,
        name: Optional[str] = None
    ) -> ConversationModel:
        """
        Create a new conversation.
        """
        conversation_id = ObjectId()
        conversation_model = ConversationModel(
            name=name or "Conversation",
            user_id=user_id,
            document_ids=document_ids,
            project_ids=project_ids,
            conversation_id=conversation_id,
            created_at=get_utc_zulu_timestamp(),
            updated_at=get_utc_zulu_timestamp()
        )
        self.conversation_repository.save(conversation_model.to_dict())
        return conversation_model

    def create_document_conversation(self, user_id: Any, document_id: Any) -> ConversationModel:
        """
        Create a conversation for a single document.
        """
        conversation_id = ObjectId()
        conversation_model = ConversationModel(
            name=str(document_id),
            document_ids=[document_id],
            user_id=user_id,
            conversation_id=conversation_id,
            created_at=get_utc_zulu_timestamp(),
            updated_at=get_utc_zulu_timestamp()
        )
        self.conversation_repository.save(conversation_model.to_dict())
        return conversation_model

    def sort_history(
        self,
        user_id: Any,
        sort_by: str,
        order: str = 'asc'
    ) -> List[ConversationModel]:
        """
        Sort the user's conversation history by a given field and order.
        """
        history_data = self.conversation_repository.get_user_conversations(user_id)
        if not history_data:
            return []

        reverse = (order == "desc")

        if sort_by == 'name':
            key_func = lambda c: c.get('name', '').lower()
        elif sort_by == 'created':
            key_func = lambda c: c.get('created_at', '')
        else:
            raise ValueError(f"Invalid sort_by: {sort_by}")

        sorted_history = sorted(history_data, key=key_func, reverse=reverse)
        return [ConversationModel.from_dict(c) for c in sorted_history]

    def get_conversation_history(self, user_id: Any) -> List[ConversationModel]:
        """
        Get all conversations for a user.
        """
        conversations = self.conversation_repository.get_user_conversations(user_id)
        if not conversations:
            return []
        return [ConversationModel.from_dict(c) for c in conversations]

    def get_conversation(self, conversation_id: Any) -> Optional[ConversationModel]:
        """
        Get a conversation by its ID.
        """
        conversation_data = self.conversation_repository.get_conversation_by_id(conversation_id)
        if not conversation_data:
            return None
        return ConversationModel.from_dict(conversation_data)

    def get_conversation_by_document_id(self, document_id: Any) -> Optional[ConversationModel]:
        """
        Get a conversation by document ID (using name as document_id).
        """
        conversation_data = self.conversation_repository.get_conversation_by_name(name=document_id)
        if not conversation_data:
            return None
        return ConversationModel.from_dict(conversation_data)

    def update_messages(self, conversation_id: Any, messages: List[Any]) -> None:
        """
        Update messages in a conversation.
        """
        self.conversation_repository.update_messages(conversation_id=conversation_id, messages=messages)

    def update_name(self, conversation_id: Any, new_name: str) -> None:
        """
        Update the name of a conversation.
        """
        self.conversation_repository.update_conversation_name(conversation_id=conversation_id, new_name=new_name)

    def rename_chat(self, conversation_id: Any, new_name: str) -> None:
        """
        Rename a chat (alias for update_name).
        """
        self.update_name(conversation_id, new_name)

    def delete_chat(self, conversation_id: Any) -> None:
        """
        Delete a conversation by its ID.
        """
        self.conversation_repository.delete_conversation(conversation_id)

    def delete_all_chats(self, user_id: Any) -> None:
        """
        Delete all conversations for a user.
        """
        self.conversation_repository.delete_all_conversations(user_id)

    def search_conversations(self, user_id: Any, search: str) -> List[Any]:
        """
        Search conversations for a user by a search term.
        """
        return self.conversation_repository.search_conversation(user_id, search)
