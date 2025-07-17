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

#test case if the instance in mongo is deleted but not in the server it creates problems
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
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=ssh_host,
            port=ssh_port,
            username=ssh_user,
            password=ssh_password
        )

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

    Args:
        remote_file_path (str): Full path to the file on the remote server.
        parent_local_folder (str): Parent directory where a subfolder will be created.
        document_name (str): Name of the subfolder to be created to store the file.
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
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=ssh_host,
            port=ssh_port,
            username=ssh_user,
            password=ssh_password
        )

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

    Args:
        file_path (str): Full path to the directory on the remote server.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    try:
        # Setup SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=ssh_host,
            port=ssh_port,
            username=ssh_user,
            password=ssh_password
        )
        #get
        remote_directory_path = os.path.dirname(file_path)
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

    Args:
        file_path (str): Full path to a file inside the directory on the remote server.

    Returns:
        bool: True if the directory was empty and deleted, False otherwise.
    """
    try:
        # Setup SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=ssh_host,
            port=ssh_port,
            username=ssh_user,
            password=ssh_password
        )

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

def retrieve_document_content(remote_file_path: str) -> bytes | None:
    """
    Retrieves a file from the remote server and returns its binary content.

    Args:
        remote_file_path (str): Full path to the file on the remote server.

    Returns:
        bytes | None: The file content in bytes if successful, otherwise None.
    """
    try:
        # Setup SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=ssh_host,
            port=ssh_port,
            username=ssh_user,
            password=ssh_password
        )

        # Open an SFTP session
        sftp = ssh.open_sftp()
        with sftp.file(remote_file_path, mode='rb') as remote_file:
            file_content = remote_file.read()

        ssh.close()

        return file_content

    except Exception as e:
        print(f"❌ Error retrieving file content: {e}")
        return None

def save_document_content(remote_file_path: str, file_content: bytes) -> bool:
    """
    Saves the provided file content to the remote server at the specified path.

    Args:
        remote_file_path (str): Full path to the file on the remote server.
        file_content (bytes): The content to write to the file.

    Returns:
        bool: True if the operation succeeded, False otherwise.
    """
    try:
        # Setup SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=ssh_host,
            port=ssh_port,
            username=ssh_user,
            password=ssh_password
        )

        # Open an SFTP session
        sftp = ssh.open_sftp()
        with sftp.file(remote_file_path, mode='wb') as remote_file:
            remote_file.write(file_content)

        ssh.close()

        print(f"✅ File successfully saved to: {remote_file_path}")
        return True

    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False

def save_embeddings(remote_index_path: str, index_buffer: io.BytesIO, meta_buffer: io.BytesIO) -> bool:
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=ssh_host,
            port=ssh_port,
            username=ssh_user,
            password=ssh_password
        )
        sftp = ssh.open_sftp()

        # Ensure directory exists
        print(1)
        remote_directory = os.path.dirname(remote_index_path)
        #TODO take care with the paths
        remote_directory = posixpath.join(remote_dir, remote_directory)
        print(remote_directory)

        print(2)
        try:
            sftp.stat(remote_directory)
            print(3)
        except IOError:
            sftp.mkdir(remote_directory)
            print(4)

        # Upload both buffers
        # Prepare full remote file paths
        print(5)
        remote_index_path = posixpath.join(remote_directory, "index.faiss")
        print(6)
        remote_meta_path = posixpath.join(remote_directory, "index.pkl")

        # Upload the FAISS index
        print(7)
        index_buffer.seek(0)
        with sftp.open(remote_index_path, 'wb') as f_index:
            print(8)
            f_index.write(index_buffer.read())

        # Upload the metadata
        print(9)
        meta_buffer.seek(0)
        with sftp.open(remote_meta_path, 'wb') as f_meta:
            print(10)
            f_meta.write(meta_buffer.read())

        sftp.close()
        ssh.close()
        return True


    except Exception as e:
        print(f"Error uploading the embeddings: {e}")
        return False




