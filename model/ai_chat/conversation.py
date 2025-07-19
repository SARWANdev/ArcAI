from langchain_community.vectorstores import FAISS
from typing import Dict, Any
from datetime import datetime
from model.document_reader.document import Document
from model.document_reader.library import Library
from model.document_reader.project import Project
from database.repository.conversation_repository import ConversationRepository
from database.repository.document_repository import DocumentDataBase
#call 015733401006 before huge changes lol

class Conversation:
    def __init__(self, user_id, document_ids:list[str]|None = None, project_ids:list[str]|None = None, messages=None):
        
        self.conversation_repository = ConversationRepository
        self.messages = messages or []
        self.initialise_system()
        self.user_id = user_id
        self.document_ids = document_ids
        self.conversation_id = self.__generate_conversation_id(user_id=user_id, document_ids=document_ids)
        self.document_database = DocumentDataBase


    def __generate_conversation_id(self, document_ids:list[str]|None, user_id):
        id = user_id
        for document_id in document_ids or []:
            id += document_id
        while self.conversation_repository.get_conversation_by_id(id):
            id += "e" 
        return id
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
            "user_id": self.user_id,
            "messages": self.messages,
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
        document_ids = []
        for project_id in project_ids:
            documents = self.document_database.get_documents_by_project(project_id=project_id)
            for document in documents:
                document_ids.append(document.)
    
    def get_vector_store(self):
        

