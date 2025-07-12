from langchain_community.vectorstores import FAISS
class Conversation:
    def __init__(self, id, vector_store:FAISS):
        self.__id = id
        
        self.__vector_store = vector_store
        self.__messages = []

    def rename(self, name):
        self.name = name

    def add_user_message(self, message:str):
        self.__messages.append({"role": "user",
                                "content": message})
    
    def add_ai_message(self, message:str):
        self.__messages.append({"role": "ai",
                                "content": message})
        
    def add_system_message(self, message: str):
        self.__messages.append({"role": "system",
                                "content": message})
        
    def __format_user_message(self, message:str, context: str)->str:
        formatted_message = f"""  

                    1. Use ONLY the context below.  
                    3. Keep answers under 4 sentences.  
                    4. if you give a factual answer which is NOT a greeting or small talk Print 2 newlines after the answer and explain where you got the message from with Source: 
                    

                    Context: {context}  

                    Question: {message}  

                    Answer:  
                    """
        return formatted_message
    
    def format_last_user_message(self, context: str):
        formatted_messages = self.__messages.copy()
        last_message = formatted_messages.pop()
        last_message_contents = last_message["content"]
        formatted_message = self.__format_user_message(last_message_contents, context=context)
        formatted_messages.append({"role": "user",
                                "content": formatted_message})
        return formatted_messages



        
    def get_messages(self):
        return self.__messages
    
    def get_vector_store(self)->FAISS:
        return self.__vector_store
