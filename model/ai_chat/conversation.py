from langchain_community.vectorstores import FAISS
from typing import Dict, Any
from datetime import datetime
from model.document_reader.document import Document
from model.document_reader.library import Library
from model.document_reader.project import Project
#call 015733401006 before huge changes lol

class Conversation:
    def __init__(self, user_id, document_id:str|None=None, project_id:str|None=None, messages = None):
        
        
        self.messages = messages or []
        self.initialise_system()
        self.document_id = document_id or None
        self.project_id = project_id or None
        self.user_id = user_id
        self.conversation_id = self.__generate_conversation_id()

    def __generate_conversation_id(self):
        if self.document_id:
            return self.document_id
        elif self. project_id:
            return self.project_id
        return self.user_id

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
                    4. IF you give a factual answer which is NOT a greeting or small talk Print 2 newlines after the answer and explain where you got the message from with Source: """)


    def to_dict(self) -> Dict[str, Any]:
        return {
            "_id": self.conversation_id,
            "user_id": self.user_id,
            "messages": self.messages,
        }
        
    def __format_user_message(self, message:str, context: str)->str:
        formatted_message = f"""                      

                    Context: {context}  

                    User Message: {message}  

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
    
    def get_vector_store(self):
        if self.document_id:
            
            #returndocument vector store
            pass
        elif self.project_id:
            # return project vector store
            pass
        #return library vs
        

        pass
