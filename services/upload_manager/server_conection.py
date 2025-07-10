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

def upload_document(local_path: str, relative_path: str, pdf_hash: str):
    # relative path is user_id/project_id

    try:
        if not os.path.exists(local_path):
            print(f"❌ Local file not found: {local_path}")
            return None

        original_extension = os.path.splitext(local_path)[1]  # Returns for example ".pdf"
        hashed_filename = f"{pdf_hash}{original_extension}"
        remote_dir_path = posixpath.join(remote_dir, relative_path)
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