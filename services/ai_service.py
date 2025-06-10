# from database.repository.conversation_repository import Chat as ConversationRepository
# from model.chat import Chat as ConversationModel

class AIService:

    __ollama_api_url:str
    __llm_name:str
    __embedding_model_name: str

    def __init__(self, ollama_url:str, llm_name:str, embedding_model_name:str):
        self.conversation_repository = ConversationRepository
        self.__ollama_api_url = ollama_url
        self.__llm_name = llm_name
        self.__embedding_model_name = embedding_model_name

    def set_ollama_url(self, ollama_url:str):
        self.__ollama_api_url = ollama_url

    def set_llm_name(self, llm_name:str):
        self.__llm_name = llm_name

    def set_embedding_model_name(self, embedding_model_name:str):
        self.__embedding_model_name = embedding_model_name

    def query(self, user_id, prompt):
        # TODO: Send prompt to LLM (e.g., GPT/Claude) prompt optionally contains context returns response object that can be streamed
        pass

    def summarize(self, document_id, user_id):
        # TODO: Extract important points from document text with a similarity search and return a summary string
        pass

    def follow_up(self, chat_id, prompt):
        # TODO: Continue previous chat session with new prompt
        pass

    def get_chat_history(self, user_id):
        # TODO: Fetch all chat sessions for the user
        pass

    def rename_chat(self, chat_id, new_title):
        # TODO: Rename the chat in DB
        pass

    def delete_chat(self, chat_id):
        # TODO: Hard-delete or soft-delete the chat session
        pass


    def embed(self, text_chunks:list[str]): 
        # TODO: FAISSfromTEXTChunks() returns FAISS
        pass

    def perform_similarity_search(self, query, vectorstore, top_k):
        pass

    

