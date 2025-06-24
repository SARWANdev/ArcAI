from langchain_community.vectorstores import FAISS
class Messages:
    __vector_store: FAISS
    __chat_id: str
    __messages = []
    def __init__(self, chat_id:str):
        self.__chat_id = chat_id

    def add_user_message(self, message:str):
        self.__messages.append({"role": "user",
                                "content": message})
    
    def add_ai_message(self, message:str):
        self.__messages.append({"role": "assistant",
                                "content": message})
        
    def add_system_message(self, message: str):
        self.__messages.append({"role": "system",
                                "content": message})
        
    def get_messages(self, most_recent_k_messages:int):
        return Messages


        
