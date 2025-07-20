import io
import zipfile

from database.repository.document_repository import DocumentDataBase
from database.repository.pdf_master_repository import PdfMasterDataBase
from services.upload_manager.server_conection import ssh_connection


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
    pdf_master_id = DocumentDataBase.get_pdf_master_id( document_id )
    file_hash = PdfMasterDataBase.get_pdf_hash( pdf_master_id )
    file_name = str(file_hash) + ".pdf"
    remote_path = DocumentDataBase.get_path( document_id )
    note_content = get_document_note( document_id )
    bib_content = get_document_bibtex( document_id )

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

def download_project(project_id):
    document_ids = ""
    #TODO: gets the docs ids from a project id
    pass

def download_multiple_documents(document_ids):
    """
    Downloads multiple documents, each in their own folder inside a ZIP.
    Returns the ZIP file as in-memory bytes.
    """
    ssh = ssh_connection()
    sftp = ssh.open_sftp()
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for doc_id in document_ids:
            # Fetch document data
            pdf_master_id = DocumentDataBase.get_pdf_master_id(doc_id)
            file_hash = PdfMasterDataBase.get_pdf_hash(pdf_master_id)
            file_name = f"{file_hash}.pdf"
            remote_path = DocumentDataBase.get_path(doc_id)
            note_content = get_document_note(doc_id)  # Already bytes
            bib_content = get_document_bibtex(doc_id)  # Already bytes

            # Create a folder for this document in the ZIP
            folder_name = f"document_{doc_id}/"

            # Add files to the folder
            zipf.writestr(f"{folder_name}note.txt", note_content)
            zipf.writestr(f"{folder_name}bibtex.bib", bib_content)
            with sftp.open(remote_path, 'rb') as pdf_file:
                zipf.writestr(f"{folder_name}{file_name}", pdf_file.read())

    zip_bytes = zip_buffer.getvalue()
    sftp.close()
    ssh.close()
    return zip_bytes

download_file =  download_file("687cecea963f806c97db3c3d")

# Optionally, save to disk for testing
with open('output.zip', 'wb') as f:
    print("hola")
    f.write(download_file)



