import os

from database.repository.document_repository import DocumentRepository
from database.repository.user_repository import UserRepository
from database.repository.project_repository import ProjectRepository
from exceptions.document_exceptions import InvalidUserIdException, \
    InvalidProjectIdException
from exceptions.base_exceptions import InvalidNameException

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB in bytes

class DocumentValidator:

    @staticmethod
    def validate_file(file):
        if not file.filename or file.filename.strip() == " ":
            raise InvalidNameException("Document", "no filename provided.")

        if len(file.filename) > 1000:
            raise InvalidNameException("Document", "filename is too long.")

        if not file.filename.endswith(".pdf"):
            raise InvalidNameException("Document", "filename must end with '.pdf'")

    @staticmethod
    def size_validator(file):
        """
        Validates that the file does not exceed the max size limit.
        :param file: file-like object (e.g. werkzeug.FileStorage, io.BytesIO, etc.)
        :raises ValueError: if file exceeds 50 MB
        """

        # Move to end of file to get size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()

        # Reset pointer to start so caller can read file as usual
        file.seek(0)

        if file_size > MAX_FILE_SIZE:
            raise ValueError(
                f"File size {file_size / (1024 * 1024):.2f} MB exceeds maximum of 50 MB"
            )

    @staticmethod
    def validate_user_id(user_id):
        if not user_id or user_id.strip() == "":
            raise InvalidUserIdException("no user id provided. ")

        user_exists = UserRepository.user_exists(user_id)
        if not user_exists:
            raise InvalidUserIdException("user id does not exist")

    @staticmethod
    def validate_project_id(project_id):
        if not project_id or project_id.strip() == "":
            raise InvalidUserIdException("no user id provided. ")

        project_exists = ProjectRepository.project_exists(project_id)
        if not project_exists:
            raise InvalidProjectIdException("project id does not exist")

    @staticmethod
    def validate_rename(new_name):
        if not new_name or new_name.strip() == "":
            raise InvalidNameException("Document", "No project name provided.")
        # Check if project name is too long
        if len(new_name.strip()) > InvalidNameException.MAX_DOCUMENT_NAME_LENGTH:
            raise InvalidNameException("Document", f"Document name cannot exceed {InvalidNameException.MAX_DOCUMENT_NAME_LENGTH} characters")

        # Check if project name is too short
        if len(new_name.strip()) < InvalidNameException.MIN_DOCUMENT_NAME_LENGTH:
            raise InvalidNameException("Document",
                f"Document name must be at least {InvalidNameException.MIN_DOCUMENT_NAME_LENGTH} character long")


