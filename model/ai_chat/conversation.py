from langchain_community.vectorstores import FAISS
from typing import Dict, Any


class Conversation:
    """
    Represents a conversation between a user and the AI assistant, including messages, associated documents, and metadata.

    :param user_id: The ID of the user participating in the conversation.
    :type user_id: str
    :param document_ids: List of document IDs associated with the conversation.
    :type document_ids: list[str]
    :param project_ids: List of project IDs whose documents are to be included.
    :type project_ids: list[str] | None
    :param messages: List of message dictionaries in the conversation.
    :type messages: list[dict] | None
    :param conversation_id: Unique identifier for the conversation.
    :type conversation_id: str | None
    :param created_at: Timestamp of when the conversation was created.
    :type created_at: Any
    :param updated_at: Timestamp of the last update to the conversation.
    :type updated_at: Any
    :param name: Name of the conversation.
    :type name: str | None
    """
    def __init__(self, user_id, document_ids: list[str] = [], 
                 document_id = None, project_ids: list[str] | None = None,
                 messages=None, conversation_id=None,
                 created_at=None, updated_at=None, name=None):
        self.name = name
        self.messages = messages or []
        self.user_id = user_id
        self.document_id = document_id,
        self.document_ids = document_ids
        self.conversation_id = conversation_id
        self.created_at = created_at or None
        self.updated_at = updated_at or None
        # If project_ids are provided, get their document_ids and add them
        if project_ids:
            project_document_ids = self.get_document_ids_from_project_ids(project_ids)
            self.document_ids.extend(project_document_ids)
        # delete duplicates document ids
        self.remove_duplicate_document_ids()

    def set_name(self, name):
        """
        Set the name of the conversation.

        :param name: The new name for the conversation.
        :type name: str
        """
        self.name = name

    def add_user_message(self, message: str):
        """
        Add a user message to the conversation.

        :param message: The message content from the user.
        :type message: str
        """
        self.messages.append({"role": "user",
                              "content": message})

    def add_ai_message(self, message: str):
        """
        Add an AI message to the conversation.

        :param message: The message content from the AI.
        :type message: str
        """
        self.messages.append({
            "role": "ai",
            "content": message
            })

    def add_system_message(self, message: str):
        """
        Add a system message to the conversation.

        :param message: The message content from the system.
        :type message: str
        """
        self.messages.append({"role": "system",
                              "content": message})

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Conversation object to a dictionary.

        :return: Dictionary representation of the conversation.
        :rtype: dict
        """
        return {
            "_id": self.conversation_id,
            "name": self.name,
            "user_id": self.user_id,
            "messages": self.messages,
            "document_id": self.document_id,
            "document_ids": self.document_ids,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Conversation":
        """
        Create a Conversation object from a dictionary.

        :param data: Dictionary containing conversation data.
        :type data: dict
        :return: Conversation object.
        :rtype: Conversation
        """
        return cls(
            name=data.get("name"),
            conversation_id=data.get("_id"),
            user_id=data.get("user_id"),
            document_id=data.get("document_id"),
            document_ids=data.get("document_ids"),
            messages=data.get("messages"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def get_document_id(self):
        return self.document_id

    def __format_user_message(self, message: str, context: str) -> str:
        """
        Format a user message with context for the AI assistant.

        :param message: The user's message.
        :type message: str
        :param context: The context to be included for the AI.
        :type context: str
        :return: Formatted message string.
        :rtype: str
        """
        formatted_message = f"""1. You are ArcAI a helpful AI Assistant for analyzing scientific papers.  \
                    2. Your job is to reply to User Message. = {message}\n                    3. IF NECESSARY look at the attached Context = {context}\n                    3. Keep answers concise but friendly.  \
                    4. IF you give a factual answer which is NOT a greeting or small talk Print 2 newlines after the answer and paste the unedited part from the context with Source: \
                    5. But again your main job is to answer the Message and only look at context if necessary\n                    6. Here's the message again: {message}\n                    """
        print(formatted_message)
                
        return formatted_message

    def format_last_user_message(self, context: str):
        """
        Format the last user message in the conversation with the provided context.

        :param context: The context to be included for the AI.
        :type context: str
        :return: List of formatted messages including the formatted last user message.
        :rtype: list[dict]
        """
        formatted_messages = self.messages.copy()
        last_message = formatted_messages.pop()
        last_message_contents = last_message["content"]
        formatted_message = self.__format_user_message(last_message_contents, context=context)
        formatted_messages.append({"role": "user",
                                   "content": formatted_message})
        return formatted_messages

    def get_messages(self):
        """
        Get the list of messages in the conversation.

        :return: List of message dictionaries.
        :rtype: list[dict]
        """
        return self.messages

    def get_document_ids_from_project_ids(self, project_ids: list[str]):
        """
        Retrieve document IDs associated with the given project IDs.

        :param project_ids: List of project IDs.
        :type project_ids: list[str]
        :return: List of document IDs.
        :rtype: list[str]
        """
        from services.document_service import DocumentService
        document_ids = []
        for project_id in project_ids:
            documents = DocumentService().get_project_documents(project_id=project_id)
            for document in documents or []:
                document_ids.append(document.document_id)
        return document_ids

    def get_vector_store(self):
        """
        Retrieve the merged vector store for all documents in the conversation.

        :return: Merged vector store object.
        :rtype: Any
        """
        from services.upload_manager.embeddings_manager import EmbeddingsManager
        from services.ai_service import AIService
        document_embeddings = []
        for document_id in self.document_ids or []:
            document_embeddings.append(EmbeddingsManager.get_embeddings(document_id=document_id))
        return AIService().merge_vector_stores(document_embeddings)

    def remove_duplicate_document_ids(self):
        """
        Remove duplicate document IDs from the conversation's document_ids list.
        """
        if self.document_ids:
            self.document_ids = list(dict.fromkeys(self.document_ids))
