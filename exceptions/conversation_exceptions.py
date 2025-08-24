from exceptions.base_exceptions import ValidationException, BusinessLogicException, InfrastructureException

class InvalidConversationName(ValidationException):
    """Invalid conversation name (Validation exception)"""

    MAX_NAME_LENGTH = 100
    MIN_NAME_LENGTH = 1

    def __init__(self, details: str = "Unspecified naming violation"):
        root_message = "Invalid conversation name"
        super().__init__(root_message, details)
        self.details = details
        self.root_message = root_message

class DuplicateConversationName(BusinessLogicException):
    """Conversation with same name already exists"""

    def __init__(self, conversation_name: str):
        root_message = "Conversation name already exists"
        details = f"Conversation '{conversation_name}' already exists in your library"
        super().__init__(root_message, details)
        self.conversation_name = conversation_name

class ConversationNotFoundError(InfrastructureException):
    """Conversation could not be found"""
    def __init__(self, root_message: str = "An infrastructure error occurred", details: str = ""):
        super().__init__(root_message, details)
        self.details = details
        self.root_message = root_message
