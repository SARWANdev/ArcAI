import hashlib
from pathlib import Path



def get_pdf_sha256(pdf_path: str) -> str:
    """
    Calculates the SHA-256 hash of a PDF file.

    Parameters:
        pdf_path (str): The file path to the PDF.

    Returns:
        str: The SHA-256 hexadecimal hash of the file.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        IOError: If there is an error reading the file.
    """
    path = Path(pdf_path)

    if not path.is_file():
        raise FileNotFoundError(f"No such file: '{pdf_path}'")

    hash_sha256 = hashlib.sha256()

    try:
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_sha256.update(chunk)
    except IOError as e:
        raise IOError(f"Error reading file '{pdf_path}': {e}")

    return hash_sha256.hexdigest()

def document_name_generator(pdf_path: str) -> str:
    #TODO developt this method that generates a name with the first 3 words of the titel , firs autor last name and date of publishin if possible
    return ""

def relative_path_generator(user_id: str, project_id: str) -> str:
    return f"{user_id}/{project_id}"