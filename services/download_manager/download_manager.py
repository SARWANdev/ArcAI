import io
import zipfile

from database.repository.document_properties_repository import DocumentPropertiesRepository
from database.repository.document_repository import DocumentDataBase
from database.repository.pdf_master_repository import PdfMasterDataBase
from database.repository.project_repository import Project as ProjectDataBase
from services.document_service import DocumentService
from services.upload_manager.server_conection import ssh_connection

#Chimnay method for front end
def download_project(project_id):
    document_ids = DocumentService().get_document_ids_from_project_id(project_id=project_id)
    doc_ids_str = []
    for doc_id in document_ids:
        doc_ids_str.append(str(doc_id))
    zip_bytes = download_multiple_documents(doc_ids_str, project_id)
    return zip_bytes

#Chimnay method for front-end
def download_project_bibtex(project_id):
    document_ids = DocumentService().get_document_ids_from_project_id(project_id=project_id)
    doc_ids_str = []
    for doc_id in document_ids:
        doc_ids_str.append(str(doc_id))

    return download_multiple_bibtex(doc_ids_str)

def get_project_note(project_id):
    project_note = ProjectDataBase.get_note(project_id).encode("utf8")
    return project_note

def get_document_note(document_id):
    note = DocumentDataBase.get_note(document_id)
    note = note.encode("utf8")
    return note

def get_document_bibtex(document_id):
    pdf_master_id = DocumentDataBase.get_pdf_master_id(document_id)
    bibtex = PdfMasterDataBase.get_bibtex(pdf_master_id)
    bibtex = bibtex.encode("utf8")
    return bibtex


def download_file(document_id):
    pdf_master_id = DocumentDataBase.get_pdf_master_id(document_id)
    file_hash = PdfMasterDataBase.get_pdf_hash(pdf_master_id)
    file_name = str(file_hash) + ".pdf"
    remote_path = DocumentDataBase.get_path(document_id)
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
    ssh = ssh_connection()
    sftp = ssh.open_sftp()
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:

        for document_id in doc_ids_str:
            doc_name = DocumentDataBase.get_name(document_id)
            bib_content = get_document_bibtex(document_id)
            zipf.writestr(f"{doc_name}_bibtex.bib", bib_content)

    zip_bytes = zip_buffer.getvalue()

    sftp.close()
    ssh.close()
    return zip_bytes


def download_multiple_documents(document_ids, project_id):
    """
    Downloads multiple documents, each in their own folder inside a ZIP.
    Returns the ZIP file as in-memory bytes.
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
            pdf_master_id = DocumentDataBase.get_pdf_master_id(doc_id)
            file_hash = PdfMasterDataBase.get_pdf_hash(pdf_master_id)
            doc_name = DocumentDataBase.get_name(doc_id)
            file_name = f"{file_hash}.pdf"
            remote_path = DocumentDataBase.get_path(doc_id)
            note_content = get_document_note(doc_id)  # Already bytes
            bib_content = get_document_bibtex(doc_id)  # Already bytes
            # Create a folder for this document in the ZIP
            folder_name = f"document_{doc_name}/"
            # Add files to the folder
            zipf.writestr(f"{folder_name}note.txt", note_content)
            zipf.writestr(f"{folder_name}bibtex.bib", bib_content)
            with sftp.open(remote_path, 'rb') as pdf_file:
                zipf.writestr(f"{folder_name}{file_name}", pdf_file.read())
    zip_bytes = zip_buffer.getvalue()
    sftp.close()
    ssh.close()
    return zip_bytes

#download_file =  download_file("687f88042fe107c0c717f9ab")
#with open('chimney.zip', 'wb') as f:
#    print("hola")
#    f.write(download_file)

#list_of_docs = ["687ced1834f028bf0cce3bd8", "687d0f1662a4b5b2b039972a", "687d0f4f5be32d07a2b5960c"]
#list_of_docs = ["687f88042fe107c0c717f9ab"]
#multiple_docs = download_multiple_documents(list_of_docs)
# Optionally, save to disk for testing
#with open('double.zip', 'wb') as f:
#    print("hola")
#    f.write(multiple_docs)




