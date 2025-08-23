from exceptions.base_exceptions import BusinessLogicException
from exceptions.base_exceptions import InfrastructureException
class AIConnectionException(BusinessLogicException):
    """Raised when AI Connection fails"""
    def __init__(self, details: str = "Unspecified LLM connection error"):
        root_message = "Couldn't connect to LLM: "
        full_message = f"{root_message}: {details}"
        super().__init__(full_message)
        self.details = details
        self.root_message = root_message

class AIGenerationException(BusinessLogicException):
    """Raised when the AI fails to generate a response."""
    def __init__(self, details: str = "Failed to generate response from LLM"):
        root_message = "AI generation error"
        full_message = f"{root_message}: {details}"
        super().__init__(full_message)
        self.details = details
        self.root_message = root_message

class AIEmbeddingException(InfrastructureException):
    """Raised when saving embeddings fails."""
    def __init__(self, details: str = "Embedding Error"):
        root_message = "AI embedding save error"
        full_message = f"{root_message}: {details}"
        super().__init__(full_message)
        self.details = details

