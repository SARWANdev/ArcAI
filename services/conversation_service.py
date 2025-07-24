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
        """
        Initialize the ConversationService.
        """
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

        :param user_id: The ID of the user creating the conversation.
        :type user_id: Any
        :param document_ids: List of document IDs associated with the conversation.
        :type document_ids: list
        :param project_ids: List of project IDs associated with the conversation. Defaults to None.
        :type project_ids: list or None
        :param name: Name of the conversation. Defaults to None.
        :type name: str or None
        :return: The created conversation model instance.
        :rtype: ConversationModel
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

    def create_document_conversation(self, user_id: Any, document_id: Any) -> ConversationModel|None:
        """
        Create a conversation for a single document.

        :param user_id: The ID of the user creating the conversation.
        :type user_id: Any
        :param document_id: The document ID to associate with the conversation.
        :type document_id: Any
        :return: The created conversation model instance.
        :rtype: ConversationModel
        """
        conversation_id = ObjectId()
        from services.document_service import DocumentService
        document = DocumentService().get_document(document_id=document_id)
        if document: 
            name = document.name
            conversation_model = ConversationModel(
                
                name=f"Conversation on {name}",
                document_ids=[document_id],
                user_id=user_id,
                conversation_id=conversation_id,
                created_at=get_utc_zulu_timestamp(),
                updated_at=get_utc_zulu_timestamp(),
                document_id=document_id
            )
            self.conversation_repository.save(conversation_model.to_dict())
            return conversation_model
        print("Couldn't find valid Document")
        

    def sort_history(
        self,
        user_id: Any,
        sort_by: str,
        order: str = 'asc'
    ) -> List[ConversationModel]:
        """
        Sort the user's conversation history by a given field and order.

        :param user_id: The ID of the user whose conversations to sort.
        :type user_id: Any
        :param sort_by: The field to sort by ('name', 'created').
        :type sort_by: str
        :param order: Sort order, either 'asc' or 'desc'. Defaults to 'asc'.
        :type order: str
        :return: Sorted list of conversation models.
        :rtype: list of ConversationModel
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

        :param user_id: The ID of the user whose conversation history to retrieve.
        :type user_id: Any
        :return: List of conversation models for the user.
        :rtype: list of ConversationModel
        """
        conversations = self.conversation_repository.get_user_conversations(user_id)
        if not conversations:
            return []
        return [ConversationModel.from_dict(c) for c in conversations]

    def get_conversation(self, conversation_id: Any) -> Optional[ConversationModel]:
        """
        Get a conversation by its ID.

        :param conversation_id: The ID of the conversation to retrieve.
        :type conversation_id: Any
        :return: The conversation model if found, else None.
        :rtype: ConversationModel or None
        """
        conversation_data = self.conversation_repository.get_conversation_by_id(conversation_id)
        if not conversation_data:
            return None
        return ConversationModel.from_dict(conversation_data)

    def get_conversation_by_document_id(self, document_id: Any) -> Optional[ConversationModel]:
        """
        Get a conversation by document ID (using name as document_id).

        :param document_id: The document ID (used as conversation name) to search for.
        :type document_id: Any
        :return: The conversation model if found, else None.
        :rtype: ConversationModel or None
        """
        conversation_data = self.conversation_repository.get_conversation_by_name(name=document_id)
        if not conversation_data:
            return None
        return ConversationModel.from_dict(conversation_data)

    def update_messages(self, conversation_id: Any, messages: List[Any]) -> None:
        """
        Update messages in a conversation.

        :param conversation_id: The ID of the conversation to update.
        :type conversation_id: Any
        :param messages: The new list of messages to set.
        :type messages: list
        :return: None
        :rtype: None
        """
        self.conversation_repository.update_messages(conversation_id=conversation_id, messages=messages)

    def update_name(self, conversation_id: Any, new_name: str) -> None:
        """
        Update the name of a conversation.

        :param conversation_id: The ID of the conversation to update.
        :type conversation_id: Any
        :param new_name: The new name for the conversation.
        :type new_name: str
        :return: None
        :rtype: None
        """
        self.conversation_repository.update_conversation_name(conversation_id=conversation_id, new_name=new_name)

    def rename_chat(self, conversation_id: Any, new_name: str) -> None:
        """
        Rename a chat (alias for update_name).

        :param conversation_id: The ID of the conversation to rename.
        :type conversation_id: Any
        :param new_name: The new name for the conversation.
        :type new_name: str
        :return: None
        :rtype: None
        """
        self.update_name(conversation_id, new_name)

    def delete_chat(self, conversation_id: Any) -> None:
        """
        Delete a conversation by its ID.

        :param conversation_id: The ID of the conversation to delete.
        :type conversation_id: Any
        :return: None
        :rtype: None
        """
        self.conversation_repository.delete_conversation(conversation_id)

    def delete_all_chats(self, user_id: Any) -> None:
        """
        Delete all conversations for a user.

        :param user_id: The ID of the user whose conversations to delete.
        :type user_id: Any
        :return: None
        :rtype: None
        """
        self.conversation_repository.delete_all_conversations(user_id)

    def search_conversations(self, user_id: Any, search: str) -> List[Any]:
        """
        Search conversations for a user by a search term.

        :param user_id: The ID of the user whose conversations to search.
        :type user_id: Any
        :param search: The search term to filter conversations.
        :type search: str
        :return: List of conversations matching the search term.
        :rtype: list
        """
        
        hits = ConversationRepository.search_conversation(user_id, search)
        if not hits:
            return []

        conversation_ids = [chat['id'] for chat in hits]
        conversation_list = []
        for id in conversation_ids:
            conversation_data = self.conversation_repository.get_conversation_by_id(id)
            conversation_model = ConversationModel.from_dict(conversation_data)
            if not conversation_model.get_document_id():
                conversation_list.append(conversation_model)
        return conversation_list
