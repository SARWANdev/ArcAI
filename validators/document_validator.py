import os

from database.repository.document_repository import DocumentRepository
from database.repository.user_repository import UserRepository
from database.repository.project_repository import Project
from exceptions.document_exceptions import InvalidDocumentNamingException, InvalidUserIdException, \
    InvalidProjectIdException, InvalidDocumentName

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB in bytes

class DocumentValidator:

    @staticmethod
    def validate_file(file):
        if not file.filename or file.filename.strip() == " ":
            raise InvalidDocumentNamingException("no filename provided.")

        if len(file.filename) > 1000:
            raise InvalidDocumentNamingException("filename is too long.")

        if not file.filename.endswith(".pdf"):
            raise InvalidDocumentNamingException("filename must end with '.pdf'")

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

        project_exists = Project.project_exists(project_id)
        if not project_exists:
            raise InvalidProjectIdException("project id does not exist")

    @staticmethod
    def validate_rename(new_name):
        if not new_name or new_name.strip() == "":
            raise InvalidDocumentName("No project name provided.")
        # Check if project name is too long
        if len(new_name.strip()) > InvalidDocumentName.MAX_NAME_LENGTH:
            raise InvalidDocumentName(f"Project name cannot exceed {InvalidDocumentName.MAX_NAME_LENGTH} characters")

        # Check if project name is too short
        if len(new_name.strip()) < InvalidDocumentName.MIN_NAME_LENGTH:
            raise InvalidDocumentName(
                f"Project name must be at least {InvalidDocumentName.MIN_NAME_LENGTH} character long")


