class AIConnectionException(Exception):
    """Raised when AI Connection fails"""
    def __init__(self, details: str = "Unspecified LLM connection error"):
        self.details = details
        self.root_message = "Couldn't connect to LLM"
        message = f"{self.root_message}: {details}"
        super().__init__(message)

class AIGenerationException(Exception):
    """Raised when the AI fails to generate a response."""
    def __init__(self, details: str = "Failed to generate response from LLM"):
        self.details = details
        self.root_message = "AI generation error"
        message = f"{self.root_message}: {details}"
        super().__init__(message)

class AIEmbeddingException(Exception):
    """Raised when saving embeddings fails."""
    def __init__(self, details: str = "Embedding Error"):
        self.details = details
        self.root_message = "AI embedding save error"
        message = f"{self.root_message}: {details}"
        super().__init__(message)

