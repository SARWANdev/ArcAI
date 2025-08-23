from exceptions.base_exceptions import BusinessLogicException, InfrastructureException

class UserNotFound(InfrastructureException):

    def __init__(self, root_message: str = "An infrastructure error occurred", details: str = ""):
        pass    