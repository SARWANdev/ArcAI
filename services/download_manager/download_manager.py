import io
import zipfile

from database.repository.document_repository import DocumentRepository
from database.repository.pdf_master_repository import PdfMasterRepository
from database.repository.project_repository import ProjectRepository
from services.document_service import DocumentService
from services.upload_manager.server_conection import ssh_connection
from utils.utils import format_filename
from exceptions.base_exceptions import NotFoundException


def download_project(project_id):
    """
    Downloads all documents in a project as a ZIP file containing the PDFs, BibTeX files, and notes.

    :param project_id: The ID of the project to download documents for.
    :type project_id: str

    :returns: The ZIP file containing the project documents, as in-memory bytes.
    :rtype: bytes
    """
    document_ids = DocumentService().get_document_ids_from_project_id(project_id=project_id)
    doc_ids_str = []
    for doc_id in document_ids:
        doc_ids_str.append(str(doc_id))
    zip_bytes = download_multiple_documents(doc_ids_str, project_id)
    return zip_bytes

def download_project_bibtex(project_id):
    """
    Downloads all BibTeX entries for documents in a project as a ZIP file.

    :param project_id: The ID of the project to download BibTeX files for.
    :type project_id: str

    :returns: The ZIP file containing the BibTeX files, as in-memory bytes.
    :rtype: bytes
    """
    document_ids = DocumentService().get_document_ids_from_project_id(project_id=project_id)
    doc_ids_str = []
    for doc_id in document_ids:
        doc_ids_str.append(str(doc_id))

    return download_multiple_bibtex(doc_ids_str)

def get_project_note(project_id):
    """
    Retrieves the project note for the specified project.

    :param project_id: The ID of the project to get the note for.
    :type project_id: str

    :returns: The project note encoded in UTF-8.
    :rtype: bytes
    """
    project_note = ProjectRepository.get_note(project_id).encode("utf8")
    return project_note

def get_document_note(document_id):
    """
    Retrieves the note for the specified document.

    :param document_id: The ID of the document to get the note for.
    :type document_id: str

    :returns: The document note encoded in UTF-8.
    :rtype: bytes
    """
    note = DocumentRepository.get_note(document_id)
    note = note.encode("utf8")
    return note

def get_document_bibtex(document_id):
    """
    Retrieves the BibTeX entry for the specified document.

    :param document_id: The ID of the document to get the BibTeX entry for.
    :type document_id: str

    :returns: The BibTeX entry encoded in UTF-8.
    :rtype: bytes
    """
    pdf_master_id = DocumentRepository.get_pdf_master_id(document_id)
    try:
        bibtex = PdfMasterRepository.get_bibtex(pdf_master_id)
        bibtex = bibtex.encode("utf8")
        return bibtex
    except Exception as e:
        raise NotFoundException("BibTeX", "requested entry")


def download_file(document_id):
    """
    Downloads a single document as a ZIP file containing the PDF, BibTeX, and note files.

    :param document_id: The ID of the document to download.
    :type document_id: str

    :returns: The ZIP file containing the document, as in-memory bytes.
    :rtype: bytes
    """
    pdf_master_id = DocumentRepository.get_pdf_master_id(document_id)
    file_hash = PdfMasterRepository.get_pdf_hash(pdf_master_id)
    document_name = format_filename( DocumentRepository.get_name(document_id) )
    #file_name = str(file_hash) + ".pdf"
    file_name = str(document_name) + ".pdf"
    remote_path = DocumentRepository.get_path(document_id)
    note_content = get_document_note(document_id)
    bib_content = get_document_bibtex(document_id)

    ssh = ssh_connection()
    sftp = ssh.open_sftp()

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:

        zipf.writestr( 'note.txt' ,note_content )

        zipf.writestr('bibtex.bib', bib_content)

        with sftp.open(remote_path, 'rb') as pdf_file:
            zipf.writestr(file_name, pdf_file.read())

    zip_bytes = zip_buffer.getvalue()
    sftp.close()
    ssh.close()
    return zip_bytes


def download_multiple_bibtex(doc_ids_str):
    """
    Downloads the BibTeX entries for multiple documents as a ZIP file.

    :param doc_ids_str: A list of document IDs to download the BibTeX entries for.
    :type doc_ids_str: list[str]

    :returns: The ZIP file containing the BibTeX entries, as in-memory bytes.
    :rtype: bytes
    """
    ssh = ssh_connection()
    sftp = ssh.open_sftp()
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:

        for document_id in doc_ids_str:
            doc_name = DocumentRepository.get_name(document_id)
            bib_content = get_document_bibtex(document_id)
            zipf.writestr(f"{doc_name}_bibtex.bib", bib_content)

    zip_bytes = zip_buffer.getvalue()

    sftp.close()
    ssh.close()
    return zip_bytes


def download_multiple_documents(document_ids, project_id):
    """
    Downloads multiple documents, each in their own folder inside a ZIP file.
    Returns the ZIP file as in-memory bytes.

    :param document_ids: A list of document IDs to download.
    :type document_ids: list[str]
    :param project_id: The project ID to associate with the documents.
    :type project_id: str

    :returns: The ZIP file containing the documents, as in-memory bytes.
    :rtype: bytes
    """
    ssh = ssh_connection()
    sftp = ssh.open_sftp()
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        project_note = get_project_note(project_id)  #TODO
        zipf.writestr( 'project_note.txt', project_note ) #TODO
        for doc_id in document_ids:
            doc_id = str(doc_id)
            # Fetch document data
            pdf_master_id = DocumentRepository.get_pdf_master_id(doc_id)
            file_hash = PdfMasterRepository.get_pdf_hash(pdf_master_id)
            doc_name =  format_filename(DocumentRepository.get_name(doc_id))
            file_name = f"{doc_name}.pdf"
            remote_path = DocumentRepository.get_path(doc_id)
            note_content = get_document_note(doc_id)  # Already bytes
            bib_content = get_document_bibtex(doc_id)  # Already bytes
            # Create a folder for this document in the ZIP
            folder_name = f"{doc_name}/"
            # Add files to the folder
            zipf.writestr(f"{folder_name}note.txt", note_content)
            zipf.writestr(f"{folder_name}bibtex.bib", bib_content)
            with sftp.open(remote_path, 'rb') as pdf_file:
                zipf.writestr(f"{folder_name}{file_name}", pdf_file.read())
    zip_bytes = zip_buffer.getvalue()
    sftp.close()
    ssh.close()
    return zip_bytes

