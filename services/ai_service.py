from database.repository.ai_repository.conversation_repository import ConversationRepository
#from model.chat import Chat as ConversationModel
import requests
import json

class AIService:

    __ollama_api_url:str
    __llm_name:str
    __embedding_model_name: str
    __DEFAULT_URL = "http://127.0.0.1:11435"
    __DEFAULT_EMBEDDING_MODEL_NAME = "nomic-embed-text"
    __DEFAULT_LLM_NAME = "gemma3"
    __GENERATE_PATH = "/api/generate"
    __CHAT_PATH = "/api/chat"

    def __init__(self, ollama_url:str|None = None, llm_name:str|None = None, embedding_model_name:str|None = None):
        self.conversation_repository = ConversationRepository
        self.__ollama_api_url = ollama_url if ollama_url else self.__DEFAULT_URL
        self.__llm_name = llm_name if llm_name else self.__DEFAULT_LLM_NAME
        self.__embedding_model_name = embedding_model_name if embedding_model_name else self.__DEFAULT_EMBEDDING_MODEL_NAME

    def set_ollama_url(self, ollama_url:str):
        self.__ollama_api_url = ollama_url

    def set_llm_name(self, llm_name:str):
        self.__llm_name = llm_name

    def set_embedding_model_name(self, embedding_model_name:str):
        self.__embedding_model_name = embedding_model_name

    def generate(self, user_id, prompt):
        #TODO: specific error messages for each possible error
        generate_url = f"{self.__DEFAULT_URL}{self.__GENERATE_PATH}"
        payload = {"model": self.__llm_name,
                    "prompt": prompt}
        try:
            response = requests.post(url=generate_url, json=payload, stream=True)
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                print(response.text)
            else:
                return response
        except Exception as e:
            print(f"Exception: {e}")
            

    def summarize(self, document_id, user_id):
        # TODO: Extract important points from document text with a similarity search and return a summary string
        pass

    def chat(self, chat_id, prompt):
        # TODO: Continue previous chat session with new prompt
        pass

    def get_chat_history(self, user_id):
        # TODO: Fetch all chat sessions for the user
        pass

    def get_chat(self, chat_id):
        # TODO: Fetch the conversation for the chat
        pass

    def rename_chat(self, chat_id, new_title):
        # TODO: Rename the chat in DB
        pass

    def delete_chat(self, chat_id):
        # TODO: Hard-delete or soft-delete the chat session
        pass

    def delete_all_chats(self, user_id):
        # TODO: Delete all chat sessions for the user
        pass


    def embed(self, text_chunks:list[str]): 

        # TODO: FAISSfromTEXTChunks() returns FAISS
        pass

    def perform_similarity_search(self, query, vectorstore, top_k):
        pass

    

