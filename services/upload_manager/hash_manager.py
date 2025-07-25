import hashlib
from pathlib import Path



def get_pdf_sha256(pdf_path: str) -> str:
    """
    Calculates the SHA-256 hash of a PDF file.

    Parameters:
    :param pdf_path: The file path to the PDF.
    :type pdf_path: str
    
    :returns: The SHA-256 hexadecimal hash of the file.
    :rtype: str

    :raises:FileNotFoundError: If the PDF file does not exist; IOError: If there is an error reading the file.
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


def relative_path_generator(user_id: str, project_id: str) -> str:
    """
    Creates a relative path for a given user and project id.

    :param user_id: A user ID.
    :type user_id: str
    :param project_ id: A user's project ID.
    :param project_id: str

    :returns: The generated relative path with the user and project id.
    :rtype: str
    """
    return f"{user_id}/{project_id}"