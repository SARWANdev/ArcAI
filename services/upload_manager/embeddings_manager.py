import io
import os
import pickle
import tempfile
import faiss
from langchain_community.vectorstores import FAISS


class EmbeddingsManager:
    @staticmethod
    def serialize_vector_store(vector_store: FAISS):
        """
        Serializes the FAISS index and metadata to in-memory byte streams.

        Returns:
            Tuple[BytesIO, BytesIO]: (faiss_index_buffer, metadata_buffer)
        """
        # --- Serialize FAISS index to temp file ---
        with tempfile.NamedTemporaryFile(delete=False) as tmp_index_file:
            temp_index_path = tmp_index_file.name

        try:
            faiss.write_index(vector_store.index, temp_index_path)

            with open(temp_index_path, "rb") as f:
                faiss_index_buffer = io.BytesIO(f.read())
                faiss_index_buffer.seek(0)
        finally:
            os.remove(temp_index_path)

        # --- Serialize metadata ---
        metadata = {
            "docstore": vector_store.docstore,
            "index_to_docstore_id": vector_store.index_to_docstore_id,
            "embedding_function": None  # Usually can't be serialized
        }

        metadata_buffer = io.BytesIO()
        pickle.dump(metadata, metadata_buffer)
        metadata_buffer.seek(0)

        return faiss_index_buffer, metadata_buffer
