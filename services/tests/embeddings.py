import io
import os
import pickle
import tempfile

from langchain_community.vectorstores import FAISS
import faiss

from services.ai_service import AIService
from services.upload_manager.server_conection import save_embeddings




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




vector_store_example = AIService().get_vector_store(["hola", "amigos", "como", "estan"])
print(vector_store_example)

ser_vector_store_example = serialize_vector_store(vector_store_example)
print(type(ser_vector_store_example))

remote_path = "117530366620837166459/687263f6d6adfb6fdfa4aa4d/b873ee2ef42e2209ef03c15d13c71b5481062a97818f0dab93d69f9fb7c718ff/b873ee2ef42e2209ef03c15d13c71b5481062a97818f0dab93d69f9fb7c718ff.pdf"


save_embeddings(remote_path, ser_vector_store_example[0], ser_vector_store_example[1])


