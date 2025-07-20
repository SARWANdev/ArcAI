import io
import os
import pickle
import posixpath
import tempfile
import faiss
from langchain_community.vectorstores import FAISS

from database.repository.document_repository import DocumentDataBase
from services.ai_service import AIService
from services.upload_manager.server_conection import ssh_connection


class EmbeddingsManager:
    @staticmethod
    def serialize_vector_store(vector_store: FAISS):
        """
        Serializes the FAISS index and metadata to in-memory byte streams.

        Returns:
            Tuple[BytesIO, BytesIO]: (faiss_index_buffer, metadata_buffer)
        """
        # --- Serialize FAISS index to temp file ---
        with tempfile.TemporaryDirectory() as temp_dir:
            vector_store.save_local(temp_dir)

            index_faiss_path = os.path.join(temp_dir, "index.faiss")
            with open(index_faiss_path, "rb") as f:
                faiss_index_buffer = io.BytesIO(f.read())
                faiss_index_buffer.seek(0)

            # Read index.pkl into memory
            index_pkl_path = os.path.join(temp_dir, "index.pkl")
            with open(index_pkl_path, "rb") as f:
                metadata_buffer = io.BytesIO(f.read())
                metadata_buffer.seek(0)


        return faiss_index_buffer, metadata_buffer

    @staticmethod
    def load_remote_faiss_index(remote_index_path: str) -> bytes | None: #ACHTUNG: this is the path of the actual document

        # Step 1: Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:

            ssh = ssh_connection()
            sftp = ssh.open_sftp()

            # Step 2: Download index.faiss and index.pkl
            for file in ["index.faiss", "index.pkl"]:
                remote_file = posixpath.join(remote_index_path, file)
                print("remote_file:  ", remote_file)
                local_file = os.path.join(temp_dir, file)
                print("local_file:  ", local_file)
                sftp.get(remote_file, local_file)

            print("temp_dir:  ", temp_dir)
            sftp.close()
            ssh.close()

            faiss_index = AIService().load_vector_store_from_path(temp_dir)


            return faiss_index

    @staticmethod
    def get_embeddings(document_id):
        path = DocumentDataBase.get_path( document_id )
        path = os.path.dirname(path)
        return EmbeddingsManager.load_remote_faiss_index(path)
