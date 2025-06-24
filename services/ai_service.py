#from database.repository.ai_repository.conversation_repository import ConversationRepository
#from model.chat import Chat as ConversationModel
import requests
from requests import Response
import json
from typing import Callable
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from model.ai_chat.messages import Messages

class AIService:

    __ollama_api_url:str
    __llm_name:str
    __embedding_model_name: str
    __DEFAULT_BASE_URL = "http://127.0.0.1:11435"
    __DEFAULT_EMBEDDING_MODEL_NAME = "nomic-embed-text"
    __DEFAULT_LLM_NAME = "gemma3"
    __GENERATE_PATH = "/api/generate"
    __CHAT_PATH = "/api/chat"

    def __init__(self, ollama_url:str|None = None, llm_name:str|None = None, embedding_model_name:str|None = None):
        #self.conversation_repository = ConversationRepository
        self.__ollama_api_url = ollama_url if ollama_url else self.__DEFAULT_BASE_URL
        self.__llm_name = llm_name if llm_name else self.__DEFAULT_LLM_NAME
        self.__embedding_model_name = embedding_model_name if embedding_model_name else self.__DEFAULT_EMBEDDING_MODEL_NAME

    def set_ollama_url(self, ollama_url:str):
        self.__ollama_api_url = ollama_url

    def set_llm_name(self, llm_name:str):
        self.__llm_name = llm_name

    def set_embedding_model_name(self, embedding_model_name:str):
        self.__embedding_model_name = embedding_model_name

    def generate(self, prompt: str,  user_id= None) -> Response|None:
        #TODO: specific error messages for each possible error
        generate_url = f"{self.__DEFAULT_BASE_URL}{self.__GENERATE_PATH}"
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
            
    def output_response_stream(self, response: Response, output_function: Callable):
        response_text = ""
        for chunk in response.iter_lines():
            chunk_content = json.loads(chunk)["response"]
            response_text += chunk_content
            output_function(response_text + "▌")



    def summarize(self, vector_store:FAISS):
        similarity_search_prompt = "Most relevant parts of this text"
        relevant_chunks = self.perform_similarity_search(vector_store=vector_store, query=similarity_search_prompt, top_k=20)
        response = self.generate(f"Summarise the following in under 50 words: {relevant_chunks}")
        return response
        pass

    def send_chat_message(self, messages:Messages, message):
        # TODO: Replace Messages with id after database exists
        messages.add_user_message(message=message)
        chat_url = f"{self.__DEFAULT_BASE_URL}{self.__CHAT_PATH}"
        response = requests.post(url=chat_url, json=messages.get_messages())
        pass

    def get_chat_history(self, user_id):
        # TODO: Fetch all chat sessions for the user
        pass

    def get_chat(self, conversation_id):
        # TODO: Fetch the conversation for the chat
        pass

    def rename_chat(self, conversation_id, new_title):
        # TODO: Rename the chat in DB
        pass

    def delete_chat(self, cconversation_id):
        # TODO: Hard-delete or soft-delete the chat session
        pass

    def delete_all_chats(self, user_id):
        # TODO: Delete all chat sessions for the user
        pass


    def get_vector_store(self, text_chunks:list[str], embedding_path:str|None=None)->FAISS: 
        embeddings = OllamaEmbeddings(base_url=self.__DEFAULT_BASE_URL, model=self.__embedding_model_name)
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        if embedding_path:
            vector_store.save_local(embedding_path)
        return vector_store


    def perform_similarity_search(self, query:str, vector_store:FAISS, top_k: int)->str:
        relevant_embeddings = vector_store.similarity_search(query=query, k=top_k)
        context = "\n\n".join(doc.page_content for doc in relevant_embeddings)
        return context

    

