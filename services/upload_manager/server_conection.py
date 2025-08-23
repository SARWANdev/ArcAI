import io

import paramiko
from scp import SCPClient
import os
import posixpath
from dotenv import load_dotenv

from exceptions.document_exceptions import InvalidServerConnectionException

load_dotenv()

remote_dir = os.getenv("REMOTE_DIR") # /home/pse03
ssh_host = os.getenv("SSH_HOST")
ssh_port = int(os.getenv("SSH_PORT"))  # convert to integer
ssh_user = os.getenv("SSH_USER")
ssh_password = os.getenv("SSH_PASSWORD")

def ssh_connection():
    """
    Establishes an SSH connection to the remote server.

    :returns: An SSH client connected to the server.
    :rtype: paramiko.SSHClient
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=ssh_host,
        port=ssh_port,
        username=ssh_user,
        password=ssh_password
    )
    return ssh

def upload_document(local_path: str, relative_path: str, pdf_hash: str):
    # relative path is user_id/project_id
    """
    Uploads a document to the remote server. It checks if the file already exists before uploading.
    
    :param local_path: The local path to the document to upload.
    :type local_path: str
    :param relative_path: The relative path on the server where the file will be stored.
    :type relative_path: str
    :param pdf_hash: The hash of the PDF, used to create the unique filename.
    :type pdf_hash: str
    
    :returns: The remote file path if upload is successful, otherwise None.
    :rtype: str | None
    """

    try:
        if not os.path.exists(local_path):
            print(f"❌ Local file not found: {local_path}")
            return None

        original_extension = os.path.splitext(local_path)[1]  # Returns for example ".pdf"
        hashed_filename = f"{pdf_hash}{original_extension}"
        remote_dir_path = posixpath.join(remote_dir, relative_path, pdf_hash)
        remote_file_path = posixpath.join(remote_dir_path, hashed_filename)

        # Setup SSH
        ssh = ssh_connection()

        # 1. Create remote directory
        ssh.exec_command(f'mkdir -p "{remote_dir_path}"')
        stdout = ssh.exec_command(f'test -f "{remote_file_path}" && echo "exists"')[1]
        exists = stdout.read().decode().strip()

        if exists == "exists":
            print(f"⚠️ File already exists on server: {remote_file_path}")
            ssh.close()

            return None
        # 2. Upload the file
        with SCPClient(ssh.get_transport()) as scp:
            scp.put(local_path, remote_file_path)

        print(f"✅ Uploaded to: {remote_file_path}")
        ssh.close()

        return remote_file_path

    except Exception as e:
        print(f"❌ Error: {e}")
        raise InvalidServerConnectionException("Document Upload Failed")


def download_document(remote_file_path: str, parent_local_folder: str, document_name: str):
    """
    Downloads a file from the remote server into a designated local subfolder,
    and renames it to match the local_folder_name (keeping the original extension).

    :param remote_file_path: The full path to the file on the remote server.
    :type remote_file_path: str
    :param parent_local_folder: The local parent folder to store the downloaded file.
    :type parent_local_folder: str
    :param document_name: The name of the folder where the document will be saved.
    :type document_name: str

    :returns: The local file path if download is successful, otherwise None.
    :rtype: str | None
    """
    try:
        # Get the file extension from the remote path
        _, file_extension = os.path.splitext(remote_file_path)

        # Full path to new local folder (inside parent folder)
        full_local_folder_path = os.path.join(parent_local_folder, document_name)

        # Create local folder if it doesn't exist
        os.makedirs(full_local_folder_path, exist_ok=True)

        # New local filename: same as local_folder_name + original extension
        renamed_file_name = f"{document_name}{file_extension}"
        local_file_path = os.path.join(full_local_folder_path, renamed_file_name)

        # Setup SSH connection
        ssh = ssh_connection()

        # Download the file
        with SCPClient(ssh.get_transport()) as scp:
            scp.get(remote_file_path, local_path=local_file_path)

        print(f"✅ Downloaded to: {local_file_path}")
        ssh.close()

        return local_file_path

    except Exception as e:
        print(f"❌ Error downloading file: {e}")
        return None

def delete_remote_directory(file_path: str):
    """
    Deletes a directory and its contents on the remote server via SSH.

    :param file_path: Path of the directory to delete.
    :type file_path: str

    :returns: True if the directory was successfully deleted, otherwise False.
    :rtype: bool
    """
    try:
        # Setup SSH connection
        ssh = ssh_connection()
        remote_directory_path = file_path
        # Build the command to delete the directory recursively
        command = f"rm -rf '{remote_directory_path}'"
        stdin, stdout, stderr = ssh.exec_command(command)

        # Wait for the command to finish and check for errors
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print(f"🗑️ Successfully deleted remote directory: {remote_directory_path}")
            ssh.close()
            return True
        else:
            error = stderr.read().decode()
            print(f"❌ Error deleting remote directory: {error}")
            ssh.close()
            return False

    except Exception as e:
        print(f"❌ SSH error deleting: {e}")
        return False

def delete_remote_directory_if_empty(file_path: str) -> bool:
    """
    Deletes a directory on the remote server only if it is empty.

    :param file_path: Path to directory to be deleted.
    :type file_path: str

    :returns: True if the directory was successfully deleted, otherwise False.
    :rtype: bool
    """
    ssh = None
    try:
        # Setup SSH connection
        ssh = ssh_connection()
        remote_directory_path = os.path.dirname(file_path)

        # Check if directory is empty
        check_command = f"if [ -d '{remote_directory_path}' ] && [ -z \"$(ls -A '{remote_directory_path}')\" ]; then echo 'EMPTY'; else echo 'NOT_EMPTY'; fi"
        stdin, stdout, stderr = ssh.exec_command(check_command)
        result = stdout.read().decode().strip()

        if result == "EMPTY":
            delete_command = f"rmdir '{remote_directory_path}'"
            stdin, stdout, stderr = ssh.exec_command(delete_command)
            exit_status = stdout.channel.recv_exit_status()

            if exit_status == 0:
                print(f"🗑️ Successfully deleted empty directory: {remote_directory_path}")
                ssh.close()
                return True
            else:
                error = stderr.read().decode()
                print(f"❌ Error deleting directory: {error}")
                ssh.close()
                return False
        else:
            print(f"ℹ️ Directory not empty: {remote_directory_path}")
            ssh.close()
            return False

    except Exception as e:
        print(f"❌ SSH error: {e}")
        return False
    finally:
        if ssh: ssh.close()

def retrieve_document_content(remote_file_path: str) -> bytes | None:
    """
    Retrieves a file from the remote server and returns its binary content.

    :param remote_file_path: Path to the file on the remote server.
    :type remote_file_path: str

    :returns: The binary content of the file if successful, otherwise None.
    :rtype: bytes | None
    """
    ssh = sftp = None
    try:
        # Setup SSH connection
        ssh = ssh_connection()
        sftp = ssh.open_sftp()

        with sftp.file(remote_file_path, mode='rb') as remote_file:
            file_content = remote_file.read()

        return file_content

    except Exception as e:
        print(f"❌ Error retrieving file content: {e}")
        return None
    finally:
        if ssh: ssh.close()
        if sftp: sftp.close()

def save_document_content(remote_file_path: str, file_content: bytes) -> bool:
    """
    Saves the provided file content to the remote server at the specified path.

    :param remote_file_path: The target address to store the file content.
    :type remote_file_path: str
    :param file_content: The bytes of the file content.
    :type file_content: bytes
    :returns: True if the file was successfully saved, otherwise False.
    :rtype: bool
    """
    ssh = sftp = None
    try:

        # Open an SFTP session
        ssh = ssh_connection()
        sftp = ssh.open_sftp()
        with sftp.file(remote_file_path, mode='wb') as remote_file:
            remote_file.write(file_content)

        print(f"✅ File successfully saved to: {remote_file_path}")
        return True

    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False
    finally:
        if ssh: ssh.close()
        if sftp: sftp.close()


def save_embeddings(remote_faiss_path: str, index_buffer: io.BytesIO, meta_buffer: io.BytesIO) -> tuple[str, str] | None:
    """
    Saves FAISS index and metadata embeddings to remote SFTP server.

    :param remote_faiss_path: Target remote directory path for embeddings.
    :type remote_faiss_path: str
    :param index_buffer: Bytes buffer containing FAISS index data.
    :type index_buffer: io.BytesIO
    :param meta_buffer: Bytes buffer containing metadata.
    :type meta_buffer: io.BytesIO
    
    :returns: Tuple containing the paths to the saved FAISS index and metadata, or None if failed.
    :rtype: tuple[str, str] | None
    """
    ssh = sftp = None
    try:
        ssh = ssh_connection()
        sftp = ssh.open_sftp()

        # Ensure directory exists
        remote_directory = os.path.dirname(remote_faiss_path)
        try:
            sftp.stat(remote_directory)
        except IOError:
            sftp.mkdir(remote_directory)

        # Upload both buffers
        # Prepare full remote file paths
        remote_faiss_path = posixpath.join(remote_directory, "index.faiss")
        remote_pkl_path = posixpath.join(remote_directory, "index.pkl")

        # Upload the FAISS index
        index_buffer.seek(0)
        with sftp.open(remote_faiss_path, 'wb') as f_index:
            f_index.write(index_buffer.read())

        # Upload the metadata
        meta_buffer.seek(0)
        with sftp.open(remote_pkl_path, 'wb') as f_meta:
            f_meta.write(meta_buffer.read())

        print(f"✅ Embeddings successfully saved to: {remote_directory}")
        return remote_faiss_path, remote_pkl_path


    except Exception as e:
        print(f"Error uploading the embeddings: {e}")
        return None
    finally:
        if ssh: ssh.close()
        if sftp: sftp.close()










