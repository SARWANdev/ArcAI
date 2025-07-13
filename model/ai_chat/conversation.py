from langchain_community.vectorstores import FAISS
class Conversation:
    def __init__(self, conversation_id=None, user_id=None, name=None, list_of_documents=None,
                  human_messages=None, ai_messages=None, vector_store=None):
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.name = name
        self.list_of_documents = list_of_documents or []
        self.human_messages = human_messages or []
        self.ai_messages = ai_messages or []
        self.vector_store = vector_store

    def rename(self, name):
        self.name = name

    def add_human_message(self, msg: str):
        self.human_messages.append(msg)

    def add_ai_message(self, msg: str):
        self.ai_messages.append(msg)
        
    def __format_user_message(self, message:str, context: str)->str:
        formatted_message = f"""  

                    1. Use the context below.  
                    3. Keep answers concise.  
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
