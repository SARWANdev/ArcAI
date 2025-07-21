from langchain_community.vectorstores import FAISS
from typing import Dict, Any
#call 015733401006 before huge changes lol

class Conversation:
    def __init__(self, user_id, document_ids:list[str]|None = None, project_ids:list[str]|None = None, messages=None, conversation_id=None, 
                 created_at = None, updated_at = None, name=None):
        self.name = name
        self.messages = messages or []
        self.user_id = user_id
        print(document_ids)
        self.document_ids = document_ids
        print(self.document_ids)
        self.conversation_id = conversation_id
        self.created_at = created_at or None
        self.updated_at = updated_at or None
    
    # If project_ids are provided, get their document_ids and add them
        if project_ids:
            project_document_ids = self.get_document_ids_from_project_ids(project_ids)
            self.document_ids.extend(project_document_ids)
        #delete duplicates document ids
        print("before duplicate",self.document_ids)
        self.remove_duplicate_document_ids()
        print("before after", self.document_ids)

    def set_name(self, name):
        self.name = name
           
            
    def add_user_message(self, message:str):
        self.messages.append({"role": "user",
                                "content": message})
    
    def add_ai_message(self, message:str):
        self.messages.append({"role": "ai",
                                "content": message})
        
    def add_system_message(self, message: str):
        self.messages.append({"role": "system",
                                "content": message})
        
    def initialise_system(self):
        self.add_system_message(f"""1. You are ArcAI a helpful AI Assistant for analyzing scientific papers.  
                    2. Your job is to reply to User Message.
                    3. If necessary look at the attached Context
                    3. Keep answers concise but friendly.  
                    4. IF you give a factual answer which is NOT a greeting or small talk Print 2 newlines after the answer and explain where you got the message from with Source: 
                    """)


    def to_dict(self) -> Dict[str, Any]:
        return {
            "_id": self.conversation_id,
            "name": self.name,
            "user_id": self.user_id,
            "messages": self.messages,
            "document_ids": self.document_ids,
            "created_at": self.created_at,
            "updated_at": self.updated_at        
        }
        
    def __format_user_message(self, message:str, context: str)->str:
        formatted_message = f"""                      

                You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
                Question: {message} 
                Context: {context} 
                Answer: 

                """
        return formatted_message
    
    def format_last_user_message(self, context: str):
        formatted_messages = self.messages.copy()
        last_message = formatted_messages.pop()
        last_message_contents = last_message["content"]
        formatted_message = self.__format_user_message(last_message_contents, context=context)
        formatted_messages.append({"role": "user",
                                "content": formatted_message})
        return formatted_messages

       
    def get_messages(self):
        return self.messages
    
    def get_document_ids_from_project_ids(self, project_ids:list[str]):
        from services.document_service import DocumentService
        document_ids = []
        for project_id in project_ids:
            documents = DocumentService().get_project_documents(project_id=project_id)
            for document in documents or []:
                document_ids.append(document.document_id)
        return document_ids
    
    def get_vector_store(self):
        from services.upload_manager.embeddings_manager import EmbeddingsManager
        print(10)
        from services.ai_service import AIService
        print(11)
        document_embeddings = []
        print(12)
        for document_id in self.document_ids or []:
            print(document_id)
            document_embeddings.append(EmbeddingsManager.get_embeddings(document_id=document_id))
            print(document_embeddings)
        print(AIService().merge_vector_stores(document_embeddings))
        return AIService().merge_vector_stores(document_embeddings)
    
    def remove_duplicate_document_ids(self):
        if self.document_ids:
            self.document_ids = list(dict.fromkeys(self.document_ids))

           

