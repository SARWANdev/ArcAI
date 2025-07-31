import io
import os
import posixpath
import tempfile
from langchain_community.vectorstores import FAISS
import platform

from database.repository.document_repository import DocumentRepository
from services.ai_service import AIService
from services.upload_manager.server_conection import ssh_connection


class EmbeddingsManager:
    operating_system = platform.system() #Linux or Windows
    @staticmethod
    def serialize_vector_store(vector_store: FAISS): ##doesn't work if user on linux??
        """
        Serializes the FAISS index and metadata to in-memory byte streams.

        :param vector_store: The FAISS vector store to serialize.
        :type vector_store: FAISS
        
        :returns: A tuple containing two in-memory byte buffers: (faiss_index_buffer, metadata_buffer).
        :rtype: tuple[io.BytesIO, io.BytesIO]
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
    def load_remote_faiss_index(remote_index_path: str) -> FAISS | None: #ACHTUNG: this is the path of the actual document
        """
        Loads a FAISS index from a remote server by downloading the index.faiss and index.pkl files.

        :param remote_index_path: The remote directory path containing the index.faiss and index.pkl files.
        :type remote_index_path: str
        
        :returns: A FAISS vector store loaded from the downloaded files, or None if the process fails.
        :rtype: FAISS | None
        """
        # Step 1: Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:

            ssh = ssh_connection()
            sftp = ssh.open_sftp()

            # Step 2: Download index.faiss and index.pkl
            for file in ["index.faiss", "index.pkl"]:
                remote_file = posixpath.join(remote_index_path, file)
                print("remote_file:  ", remote_file)
                
                local_file = os.path.join(temp_dir, file)
                # Example usage, replace with actual logic if needed

                
                print("local_file:  ", local_file)
                sftp.get(remote_file, local_file)

            print("temp_dir:  ", temp_dir)
            sftp.close()
            ssh.close()

            faiss_index = AIService().load_vector_store_from_path(temp_dir)


            return faiss_index

    @staticmethod
    def get_embeddings(document_ids:list[str]):
        """
        Retrieves the FAISS embeddings for a document from the database.

        :param document_ids: The IDs of the document to retrieve embeddings for.
        :type document_ids: list(str)
        
        :returns: The FAISS vector stores associated with the documents, or [] if not found.
        :rtype: list[FAISS] | []
        """
        paths = []
        for document_id in document_ids:
            path = DocumentRepository.get_path(document_id)
            path = os.path.dirname(path)
            paths.append(path)
        paths = list(set(paths))
        embeddings = []
        for path in paths:
            embeddings.append(EmbeddingsManager.load_remote_faiss_index(path))    
        return embeddings
    
