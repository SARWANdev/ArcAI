from exceptions.base_exceptions import BusinessLogicException, InfrastructureException


class UserNotFound(InfrastructureException):
    def __init__(self, user_id: str):
        root_message = "User does not exist"
        details = f"User with ID {user_id} does not exist in the database"
        super().__init__(root_message, details)
        self.user_id = user_id