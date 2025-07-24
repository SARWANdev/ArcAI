import requests
from requests import Response
import json
from typing import Callable
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from database.repository.conversation_repository import ConversationRepository
import os
from dotenv import load_dotenv
load_dotenv()

class AIService:
    """
    AIService provides an interface for interacting with language models and embedding models via HTTP APIs.
    It supports generating text, handling chat conversations, summarizing content, and managing vector stores
    for similarity search. The service is configurable for different model names and base URLs.
    Attributes:
        __DEFAULT_BASE_URL (str): Default URL for the API endpoint.
        __DEFAULT_EMBEDDING_MODEL_NAME (str): Default embedding model name.
        __DEFAULT_LLM_NAME (str): Default language model name.
        __GENERATE_PATH (str): API path for text generation.
        __CHAT_PATH (str): API path for chat interactions.
    Methods:
        __init__(base_url: str | None = None, llm_name: str | None = None, embedding_model_name: str | None = None):
            Initializes the AIService with optional custom base URL, LLM name, and embedding model name.
        set_ollama_url(ollama_url: str):
            Sets the Ollama API URL.
        set_llm_name(llm_name: str):
            Sets the language model name.
        set_embedding_model_name(embedding_model_name: str):
            Sets the embedding model name.
        generate(prompt: str, user_id=None) -> Response | None:
            Sends a prompt to the language model and returns the response.
        send_chat_message(question: str, conversation: Conversation):
            Sends a chat message with context retrieved from similarity search.
        send_system_message(system_message: str, conversation: Conversation):
            Sends a system message to the chat API.
        output_generate_response(response, output_function: Callable):
            Streams and outputs the response from the generate endpoint.
        output_chat_response(response, output_function: Callable):
            Streams and outputs the response from the chat endpoint.
        summarize(vector_store: FAISS):
            Summarizes the most relevant parts of the text in the vector store.
        get_chat_history(user_id):
            Retrieves all chat sessions for a user. (Not implemented)
        get_chat(conversation_id):
            Retrieves a specific chat conversation. (Not implemented)
        rename_chat(conversation_id, new_title):
            Renames a chat session. (Not implemented)
        delete_chat(conversation_id):
            Deletes a chat session. (Not implemented)
        delete_all_conversations(user_id):
            Deletes all chat sessions for a user. (Not implemented)
        get_vector_store(text_chunks: list[str], embedding_path: str | None = None) -> FAISS:
            Creates a FAISS vector store from text chunks using the embedding model.
        __perform_similarity_search(query: str, vector_store: FAISS, top_k: int) -> str:
            Performs a similarity search in the vector store and returns the most relevant context.
    """
    
    __DEFAULT_BASE_URL = os.getenv("OLLAMA_DEFAULT_BASE_URL", "http://127.0.0.1:11435") #TODO:Change this to the server one on the server
    __DEFAULT_EMBEDDING_MODEL_NAME = os.getenv("OLLAMA_DEFAULT_EMBEDDING_MODEL", "nomic-embed-text")
    __DEFAULT_LLM_NAME = os.getenv("OLLAMA_DEFAULT_LLM", "gemma3")
    __GENERATE_PATH = "/api/generate"
    __CHAT_PATH = "/api/chat"
    from model.ai_chat.conversation import Conversation

    


    def __init__(self, base_url:str|None = None, llm_name:str|None = None, embedding_model_name:str|None = None):
        self.conversation_repository = ConversationRepository
        self.__llm_name = llm_name if llm_name else self.__DEFAULT_LLM_NAME
        self.__embedding_model_name = embedding_model_name if embedding_model_name else self.__DEFAULT_EMBEDDING_MODEL_NAME
        self.__base_url = base_url if base_url else self.__DEFAULT_BASE_URL
        self.embeddings = OllamaEmbeddings(base_url=self.__DEFAULT_BASE_URL, model=self.__DEFAULT_EMBEDDING_MODEL_NAME, show_progress=True)

    def set_ollama_url(self, ollama_url:str):
        self.__ollama_api_url = ollama_url

    def set_llm_name(self, llm_name:str):
        self.__llm_name = llm_name

    def set_embedding_model_name(self, embedding_model_name:str):
        self.__embedding_model_name = embedding_model_name

    def generate(self, prompt: str,  user_id= None) -> Response|None:
        """
        Sends a prompt to the language model API and returns the response.
        Args:
            prompt (str): The input prompt to generate a response for.
            user_id (Optional[Any], optional): The user identifier. Defaults to None.
        Returns:
            Response | None: The HTTP response object if the request is successful, otherwise None.
        Notes:
            - Prints error messages for non-200 HTTP responses and exceptions.
            - TODO: Implement specific error messages for each possible error.
        """
        generate_url = f"{self.__base_url}{self.__GENERATE_PATH}"
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

    def send_chat_message(self, question: str, conversation: Conversation):
        """
        Sends a chat message to the AI chat service using the provided question and conversation context.
        Args:
            question (str): The user's question or message to send to the chat service.
            conversation (Conversation): The current conversation object, used to retrieve context, older messages and format the message.
        Returns:
            requests.Response: The HTTP response object from the chat service API.
        Notes:
            - Performs a similarity search to retrieve relevant context from the conversation's vector store.
            - Formats the payload with the model name and the latest user message, including context.
            - Sends the request as a streaming POST to the chat service endpoint.
        """
        # TODO: Replace Messages with id after database exists
        vector_store = conversation.get_vector_store()
        chat_url = f"{self.__base_url}{self.__CHAT_PATH}"
        context = self.__perform_similarity_search(query=question, vector_store=vector_store, top_k=5)
        
        payload = {"model": self.__llm_name,
                    "messages": conversation.format_last_user_message(context=context),
                    }
        response = requests.post(url=chat_url, json=payload, stream=True)
        print("context", response)
        return response
        
    def send_system_message(self, system_message:str, conversation: Conversation):
        """
        Sends a system message to the chat endpoint for a given conversation.

        Args:
            system_message (str): The system message content to be sent.
            conversation (Conversation): The conversation object to which the system message is related.

        Returns:
            None

        Note:
            This method sends a POST request to the chat endpoint with the specified system message.
        """
        chat_url = f"{self.__base_url}{self.__CHAT_PATH}"
        payload = {"model": self.__llm_name,
                    "messages": {"role": "system",
                                "content": system_message}
                    }
        requests.post(url=chat_url, json=payload, stream=False)

            
            
    def output_streaming_response(self, response, output_function: Callable, mode: str = "chat"):
        """
        Processes a streaming response (either generate or chat), incrementally building the response text and invoking an output function with partial results.

        Args:
            response: The response object, expected to be an instance of `Response` that supports the `iter_lines()` method yielding JSON strings.
            output_function (Callable): A function that takes a string argument, called with the progressively built response text plus a cursor ("▌") during streaming, and with the final response text after completion.
            mode (str): Either "generate" or "chat". Determines how to extract the content from each chunk.

        Returns:
            str: The complete response text assembled from all streamed chunks.
        """
        response_text = ""
        if isinstance(response, Response):
            for chunk in response.iter_lines():
                data = json.loads(chunk)
                if mode == "generate":
                    chunk_content = data.get("response", "")
                elif mode == "chat":
                    chunk_content = data.get("message", {}).get("content", "")
                else:
                    chunk_content = ""
                response_text += chunk_content
                output_function(response_text + "▌")
        output_function(response_text)
        return response_text



    def summarize(self, vector_store:FAISS):
        """
        Generates an objective summary of the most relevant parts of the text stored in the given FAISS vector store.

        Args:
            vector_store (FAISS): The FAISS vector store containing text data to be summarized.

        Returns:
            str: An objective summary of the most relevant text chunks, limited to 50 words.
        """
        similarity_search_prompt = "Most relevant parts of this text"
        relevant_chunks = self.__perform_similarity_search(vector_store=vector_store, query=similarity_search_prompt, top_k=5)
        response = self.generate(f"Give me an objective summary of the following in 50 words: {relevant_chunks}")
        return response
        

    def get_vector_store(self, text_chunks:list[str], embedding_path:str|None=None)->FAISS: 
        """
        Creates a FAISS vector store from a list of text chunks using Ollama embeddings.

        Args:
            text_chunks (list[str]): A list of text strings to be embedded and stored in the vector store.
            embedding_path (str | None, optional): Path to save the vector store locally. If None, the vector store is not saved.

        Returns:
            FAISS: The created FAISS vector store containing the embedded text chunks.
        """
        vector_store = FAISS.from_texts(text_chunks, embedding=self.embeddings)
        if embedding_path:
            vector_store.save_local(embedding_path)
        return vector_store


    def __perform_similarity_search(self, query:str, vector_store:FAISS, top_k: int)->str:
        """
        Performs a similarity search on the provided FAISS vector store using the given query and returns the concatenated content of the top matching documents.

        Args:
            query (str): The query string to search for similar documents.
            vector_store (FAISS): The FAISS vector store instance to search within.
            top_k (int): The number of top similar documents to retrieve.

        Returns:
            str: The concatenated page content of the top matching documents, separated by double newlines.
        """
        relevant_embeddings = vector_store.similarity_search(query=query, k=top_k)
        context = "\n\n".join(doc.page_content for doc in relevant_embeddings)
        return context
    
    
    def load_vector_store_from_path(self, embedding_path:str):
        loaded_vector_store = FAISS.load_local(
        folder_path=embedding_path, embeddings=self.embeddings, allow_dangerous_deserialization=True
        )
        return loaded_vector_store
    
    def merge_vector_stores(self, vector_stores: list[FAISS]) -> FAISS:
        """
        Merges multiple FAISS vector stores into a single consolidated vector store.
        
        Args:
            vector_stores (list[FAISS]): A list of FAISS vector stores to be merged.
            
        Returns:
            FAISS: A single merged FAISS vector store containing all documents from the input stores.
            
        Raises:
            ValueError: If the input list is empty or contains non-FAISS objects.
        """
        if not vector_stores:
            raise ValueError("Cannot merge empty list of vector stores")
        
        if len(vector_stores) == 1:
            return vector_stores[0]
        
        # Start with the first vector store
        merged_vector_store = vector_stores[0]
        
        # Merge each subsequent vector store
        for i in range(1, len(vector_stores)):
            try:
                merged_vector_store.merge_from(vector_stores[i])
            except Exception as e:
                print(f"Error merging vector store {i}: {e}")
                continue
        
        return merged_vector_store

    def merge_and_save_vector_stores(self, vector_stores: list[FAISS], save_path: str) -> FAISS:
        """
        Merges multiple FAISS vector stores and saves the result to a specified path.
        
        Args:
            vector_stores (list[FAISS]): A list of FAISS vector stores to be merged.
            save_path (str): Path where the merged vector store will be saved.
            
        Returns:
            FAISS: The merged vector store.
        """
        merged_store = self.merge_vector_stores(vector_stores)
        merged_store.save_local(save_path)
        return merged_store
    
    def generate_conversation_name(self, conversation:Conversation)->str:
        from database.repository.document_repository import DocumentDataBase
        messages = str(conversation.get_messages())
        document_ids = conversation.document_ids
        merged_bibtex = ""
        for document_id in document_ids:
            bibtex = DocumentDataBase.get_bibtex_by_document_id(document_id=document_id)
            merged_bibtex+=bibtex
            
        prompt = f"""1. Make a Title for a Conversation with the following human messages:{messages} Make sure that the generated title is influenced by the given messages.
                     2. The Question was asked in the context of multiple documents. Here is the merged bibtex of all the documents: {merged_bibtex} make sure that the title has a simple reference to the multiple papers in the context.
                    3. Make sure that the conversation references the Documents and is very strongly linked to the User Message.
                    4. Only give one output without any extra information because your response will be used without any further checks in the backend
                    5. Make the title scientific and concise and between 10 to 15 words"""

        response = self.generate(prompt=prompt)
        name = self.output_streaming_response(response=response, output_function=len, mode="generate")
        return name
    










