from database.repository.document_repository import DocumentRepository
from database.repository.project_repository import Project
from exceptions.document_exceptions import InvalidDocumentNamingException, InvalidUserIdException, \
    InvalidProjectIdException


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
    def validate_user_id(user_id):
        if not user_id or user_id.strip() == "":
            raise InvalidUserIdException("no user id provided. ")

        user_exists = DocumentRepository.user_exists(user_id)
        if not user_exists:
            raise InvalidUserIdException("user id does not exist")

    @staticmethod
    def validate_project_id(project_id):
        if not project_id or project_id.strip() == "":
            raise InvalidUserIdException("nno user id provided. ")

        project_exists = Project.project_exists(project_id)
        if not project_exists:
            raise InvalidProjectIdException("project id does not exist")



