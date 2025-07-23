from database.repository.conversation_repository import ConversationRepository
from model.ai_chat.conversation import Conversation as ConversationModel
from bson import ObjectId
from database.repository.date_time_utils import get_utc_zulu_timestamp


class ConversationService:

    def __init__(self):
        self.conversation_repository = ConversationRepository

    def create_conversation(self, user_id, document_ids, project_ids=None, name="Shrawan"):
        conversation_id = ObjectId()
        conversation_model = ConversationModel(
            name=name,
            user_id=user_id,
            document_ids=document_ids,
            project_ids=project_ids,
            conversation_id=conversation_id,
            created_at=get_utc_zulu_timestamp(),
            updated_at=get_utc_zulu_timestamp()
        )
        self.conversation_repository.save(conversation_model.to_dict())
        return conversation_model
    
    def create_document_conversation(self, user_id, document_id):
        conversation_id = ObjectId()
       
        conversation_model = ConversationModel(
            name=document_id,
            document_ids=[document_id],
            user_id=user_id,
            conversation_id=conversation_id,
            created_at=get_utc_zulu_timestamp(),
            updated_at=get_utc_zulu_timestamp()
        )
        print("gonna save")
        self.conversation_repository.save(conversation_model.to_dict())
        print("done")
        return conversation_model


    def sort_history(self, user_id, sort_by, order='asc'):
        history_data = self.conversation_repository.get_user_conversations(user_id)
        if not history_data:
            return[]

        reverse = (order == "desc") 

        #Choose key
        if sort_by == 'name':
            key_func = lambda c: c.get('name', '').lower()
        elif sort_by == 'created':
            key_func = lambda c: c.get('created_at', '')
        elif sort_by == 'updated':
            key_func = lambda c: c.get('updated_at', '')
        else:
            raise ValueError(f"Invalid sort_by: {sort_by}")
        
        # Sort in Python
        sorted_history = sorted(history_data, key=key_func, reverse=reverse)

        #Map to ConversationModel
        conversations_list = []
        for c in sorted_history:
            conversation_model = ConversationModel.from_dict(c)
            conversations_list.append(conversation_model)
        
        return conversations_list


    def get_conversation_history(self, user_id):
        conversations = ConversationRepository.get_user_conversations(user_id)
        if not conversations:
            return None
        history = []
        for conversation_data in conversations:
            conversation_model = ConversationModel(
                name=conversation_data.get("name"),
                conversation_id=conversation_data.get("_id"),
                user_id=conversation_data.get("user_id"),
                document_ids=conversation_data.get("document_ids"),
                messages=conversation_data.get("messages"),
                created_at=conversation_data.get("created_at"),
                updated_at=conversation_data.get("updated_at")
            )
            history.append(conversation_model)
        return history

    def get_conversation(self, conversation_id):
        conversation_data = ConversationRepository.get_conversation_by_id(conversation_id)
        if not conversation_data:
            return None
        conversation_model = ConversationModel(
            conversation_id=conversation_data.get("_id"),
            user_id=conversation_data.get("user_id"),
            messages=conversation_data.get("messages"),
            document_ids=conversation_data.get("document_ids")
        )
        return conversation_model
    
    def get_conversation_by_document_id(self, document_id):
        conversation_data = ConversationRepository.get_conversation_by_name(name=document_id)
        if not conversation_data:
            return None
        conversation_model = ConversationModel(
            conversation_id=conversation_data.get("_id"),
            user_id=conversation_data.get("user_id"),
            messages=conversation_data.get("messages"),
            document_ids=conversation_data.get("document_ids")
        )
        return conversation_model

    def update_messages(self, conversation_id, messages):
        self.conversation_repository.update_messages(conversation_id=conversation_id, messages=messages)

    def update_name(self, conversation_id, new_name):
        self.conversation_repository.update_conversation_name(conversation_id=conversation_id, new_name=new_name)

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
