import io

import paramiko
from scp import SCPClient
import os
import posixpath
from dotenv import load_dotenv

load_dotenv()

remote_dir = os.getenv("REMOTE_DIR") # /home/pse03
ssh_host = os.getenv("SSH_HOST")
ssh_port = int(os.getenv("SSH_PORT"))  # convert to integer
ssh_user = os.getenv("SSH_USER")
ssh_password = os.getenv("SSH_PASSWORD")

def ssh_connection():
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
        return None


def download_document(remote_file_path: str, parent_local_folder: str, document_name: str):
    """
    Downloads a file from the remote server into a designated local subfolder,
    and renames the file to match the local_folder_name (keeping the original extension).


    :remote_file_path (str): Full path to the file on the remote server.
    :parent_local_folder (str): Parent directory where a subfolder will be created.
    :document_name (str): Name of the subfolder to be created to store the file.
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
    Deletes a directory and its contents on a remote server via SSH.

    :param file_path: To be deleted
    :return: True if directory was successfully deleted
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
    Deletes a directory on a remote server via SSH only if it is empty.

    :param file_path: Path to directory to be deleted.
    :return: True if the directory was successfully deleted.
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

    :param remote_file_path: path to the file on the remote server.
    :return: Bytes of the content of the file.
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

    :param remote_file_path: Target address to store the file content
    :param file_content: bytes of the file content
    :return: True if file was successfully saved.
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

    :param remote_faiss_path: Target remote directory path for embeddings
    :param index_buffer: Bytes buffer containing FAISS index data
    :param meta_buffer: Bytes buffer containing metadata
    :return: Tuple of (remote_faiss_path, remote_pkl_path) if successful, None otherwise
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










