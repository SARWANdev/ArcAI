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
from exceptions.ai_exceptions import AIConnectionException, AIGenerationException, AIEmbeddingException



class AIService:
    """
    AIService provides an interface for interacting with language models and embedding models via HTTP APIs.
    It supports generating text, handling chat conversations, summarizing content, and managing vector stores
    for similarity search. The service is configurable for different model names and base URLs.
    
    """
    
    __DEFAULT_BASE_URL = os.getenv("OLLAMA_DEFAULT_BASE_URL", "http://127.0.0.1:11435") #TODO:Change this to the server one on the server
    __DEFAULT_EMBEDDING_MODEL_NAME = os.getenv("OLLAMA_DEFAULT_EMBEDDING_MODEL", "nomic-embed-text")
    __DEFAULT_LLM_NAME = os.getenv("OLLAMA_DEFAULT_LLM", "gemma3")
    __GENERATE_PATH = "/api/generate"
    __CHAT_PATH = "/api/chat"
    from model.ai_chat.conversation import Conversation

    


    def __init__(self, base_url:str|None = None, llm_name:str|None = None, embedding_model_name:str|None = None):
        """
        Initializes the AIService with optional custom base URL, LLM name, and embedding model name.
        
        :param base_url: Optional custom base URL for the API.
        :type base_url: str|None, default None
        :param llm_name: Optional name for the language model to use.
        :type llm_name: str|None, default None
        :param embedding_model_name: Optional name for the embedding model.
        :type embedding_model_name: str|None, default None
        """
        self.conversation_repository = ConversationRepository
        self.__llm_name = llm_name if llm_name else self.__DEFAULT_LLM_NAME
        self.__embedding_model_name = embedding_model_name if embedding_model_name else self.__DEFAULT_EMBEDDING_MODEL_NAME
        self.__base_url = base_url if base_url else self.__DEFAULT_BASE_URL
        self.embeddings = OllamaEmbeddings(base_url=self.__DEFAULT_BASE_URL, model=self.__DEFAULT_EMBEDDING_MODEL_NAME, show_progress=True)

    def set_ollama_url(self, ollama_url:str):
        """
        Sets the Ollama API URL.
        
        :param ollama_url: The URL to the Ollama API.
        :type ollama_url: str
        """
        self.__ollama_api_url = ollama_url

    def set_llm_name(self, llm_name:str):
        """
        Sets the name for the language model.
        
        :param llm_name: The name of the language model to use.
        :type llm_name: str
        """
        self.__llm_name = llm_name

    def set_embedding_model_name(self, embedding_model_name:str):
        """
        Sets the name for the embedding model.
        
        :param embedding_model_name: The name of the embedding model to use.
        """
        self.__embedding_model_name = embedding_model_name

    def generate(self, prompt: str, user_id=None) -> Response | None:
        """
        Sends a prompt to the language model API and returns the response.

        :param prompt: The input prompt to generate a response for.
        :type prompt: str
        :param user_id: The user identifier (optional).

        :returns: The HTTP response object if the request is successful, otherwise None.
        :rtype: Response|None

        :raises: AIServiceError: In case of errors during the request.
        """
        generate_url = f"{self.__base_url}{self.__GENERATE_PATH}"
        payload = {"model": self.__llm_name, "prompt": prompt}
        try:
            response = requests.post(url=generate_url, json=payload, stream=True)
            if response.status_code != 200:
                # Log the error details internally if needed
                print(f"AIService generate error: {response.status_code}")
                # Raise sanitized error for the frontend or caller
                raise AIGenerationException("Failed to generate response from language model.")
            return response
        except requests.RequestException:
            raise AIConnectionException("Network error while contacting language model.")
        except Exception:
            raise AIConnectionException("Unexpected error during language model generation.")

    def send_chat_message(self, question: str, conversation: Conversation):
        """
         Sends a chat message to the AI chat service with context from the current conversation.
        
        :param question: The user's question to send.
        :type question: str
        :param conversation: The current conversation object that provides context.
        :type conversation: Conversation
        
        :returns: The HTTP response object from the chat service API.

        Notes:
            - Performs a similarity search to retrieve relevant context from the conversation's vector store.
            - Formats the payload with the model name and the latest user message, including context.
            - Sends the request as a streaming POST to the chat service endpoint.
        """
        try:
            vector_store = conversation.get_vector_store()
            chat_url = f"{self.__base_url}{self.__CHAT_PATH}"
            context = self.__perform_similarity_search(query=question, vector_store=vector_store, top_k=5)
            
            payload = {"model": self.__llm_name,
                        "messages": conversation.format_last_user_message(context=context),
                        }
            response = requests.post(url=chat_url, json=payload, stream=True)
            if response.status_code != 200:
                print(f"AIService send_chat_message error: {response.status_code}, {response.text}")
                raise AIGenerationException("Failed to get chat response from language model.")
            return response
        except AIGenerationException:
            raise AIGenerationException("Couldn't perform Similarity Search, LLM maybe offline.")        
        except requests.Timeout:
            raise AIConnectionException("The request to the language model timed out.")
        except requests.RequestException as e:
            print(f"AIService network error in send_chat_message: {str(e)}")
            raise AIConnectionException("Network error while contacting chat service.")
        except Exception as e:
            print(e)
            print(f"AIService unexpected error in send_chat_message: {str(e)}")
            raise AIConnectionException("Unexpected error during chat message processing.")
        


            
            
    def output_streaming_response(self, response, output_function: Callable, mode: str = "chat"):
        """
        Processes a streaming response (either generate or chat), 
        incrementally building the response text and invoking an output function with partial results.

        Args:
        :param response: The response object, expected to be an instance of `Response` 
            that supports the `iter_lines()` method yielding JSON strings.
        :param output_function: A function that takes a string argument, 
            called with the progressively built response text plus a cursor ("▌") during streaming, 
            and with the final response text after completion.
        :type output_function: Callable
        :parma mode: Either "generate" or "chat". Determines how to extract the content from each chunk.
        :type mode: str

        :returns: The complete response text assembled from all streamed chunks.
        :rtype: str

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




    def get_vector_store(self, text_chunks: list[str], embedding_path: str | None = None) -> FAISS:
        """
        Creates a FAISS vector store from a list of text chunks using Ollama embeddings.

        :param text_chunks: A list of text strings to be embedded and stored in the vector store.
        :type text_chunks: list[str]
        :param embedding_path: Path to save the vector store locally. If None, the vector store is not saved.
        :type embedding_path: str | None, optional

        :returns: The created FAISS vector store containing the embedded text chunks.
        :rtype: FAISS

        :raises: AIServiceError: If vector store creation or saving fails.
        """
        try:
            vector_store = FAISS.from_texts(text_chunks, embedding=self.embeddings)
            if embedding_path:
                try:
                    vector_store.save_local(embedding_path)
                except Exception:
                    raise AIEmbeddingException("Failed to save generated embedding.")
            return vector_store
        except Exception:
            raise AIEmbeddingException("Failed to embed document.")
        
    
    def load_vector_store_from_path(self, embedding_path:str):
        try:
            loaded_vector_store = FAISS.load_local(
            folder_path=embedding_path, embeddings=self.embeddings, allow_dangerous_deserialization=True
            )
            return loaded_vector_store
        except Exception:
            raise AIEmbeddingException("Failed to load embeddings.")

    
    def merge_vector_stores(self, vector_stores: list[FAISS]) -> FAISS:
        """
        Merges multiple FAISS vector stores into a single consolidated vector store.
        
        :param vector_stores: A list of FAISS vector stores to be merged.
        :type vector_stores: list[FAISS]
            
        :returns: A single merged FAISS vector store containing all documents from the input stores.
        :rtype: list[FAISS]

        :raises: ValueError: If the input list is empty or contains non-FAISS objects.
        """
        if not vector_stores:
            raise AIEmbeddingException("Cannot merge empty list of embeddings")
        
        if len(vector_stores) == 1:
            return vector_stores[0]
        
        # Start with the first vector store
        merged_vector_store = vector_stores[0]
        
        # Merge each subsequent vector store
        for i in range(1, len(vector_stores)):
            try:
                merged_vector_store.merge_from(vector_stores[i])
            except Exception:
                raise AIEmbeddingException("Error merging embeddings.")
                continue
        
        return merged_vector_store

    
    def generate_conversation_name(self, conversation:Conversation)->str:
        """
        Generate a conversation based on its messages and a given prompt.

        :param conversation: The conversation to be named.
        :type conversation: Conversation

        :returns: The generated name.
        :rtype: str 
        """
        try:
            from database.repository.document_repository import DocumentRepository
            messages = str(conversation.get_messages())
            document_ids = conversation.document_ids
            merged_bibtex = ""
            for document_id in document_ids:
                bibtex = DocumentRepository.get_bibtex_by_document_id(document_id=document_id)
                merged_bibtex+=bibtex
                
            prompt = f"""1. Make a Title for a Conversation with the following human messages:{messages} Make sure that the generated title is influenced by the given messages.
                        2. The Question was asked in the context of multiple documents. Here is the merged bibtex of all the documents: {merged_bibtex} make sure that the title has a simple reference to the multiple papers in the context.
                        3. Make sure that the conversation references the Documents and is very strongly linked to the User Message.
                        4. Only give one output without any extra information because your response will be used without any further checks in the backend
                        5. Make the title scientific and concise and between 10 to 15 words and under 80 characters
                        6. Again it is very importand that the title is under 80 words. """
            
            response = self.generate(prompt=prompt)
            name = self.output_streaming_response(response=response, output_function=len, mode="generate")
            return name
        except Exception:
            raise AIConnectionException("Connection Timed out.")
    
    
    def __perform_similarity_search(self, query:str, vector_store:FAISS, top_k: int)->str:
        """
        Performs a similarity search within the given vector store to find relevant content.
        
        :param query: The query to search for in the vector store.
        :type query: str
        :param vector_store: The vector store to perform the search in.
        :type vector_store: FAISS
        :param top_k: Number of top results to retrieve.
        :type top_k: int
        
        :returns: The concatenated content of the top matching documents.
        :rtype: str
        """
        relevant_embeddings = vector_store.similarity_search(query=query, k=top_k)
        context = "\n\n".join(doc.page_content for doc in relevant_embeddings)
        return context
    

    










