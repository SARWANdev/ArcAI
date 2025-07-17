import io
import pickle
import sys
import os
# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from langchain_community.vectorstores import FAISS



from services.ai_service import AIService
from services.upload_manager.server_conection import save_embeddings




def serialize_vector_store(vector_store: FAISS):

    faiss_index_buffer = io.BytesIO()
    metadata_buffer = io.BytesIO()

    # Save FAISS index
    vector_store.index.write_to_buffer(faiss_index_buffer)
    faiss_index_buffer.seek(0)

    # Save metadata (e.g. documents, ids, etc.)
    pickle.dump(vector_store.docstore, metadata_buffer)
    metadata_buffer.seek(0)

    return faiss_index_buffer, metadata_buffer




vector_store_example = AIService().get_vector_store(["hola", "amigos", "como", "estan"])
#print(vector_store_example)

ser_vector_store_example = serialize_vector_store(vector_store_example)
print(ser_vector_store_example)

#remote_path = "117530366620837166459/687263f6d6adfb6fdfa4aa4d/b873ee2ef42e2209ef03c15d13c71b5481062a97818f0dab93d69f9fb7c718ff/b873ee2ef42e2209ef03c15d13c71b5481062a97818f0dab93d69f9fb7c718ff.pdf"


#save_embeddings(remote_path, ser_vector_store_example[0], ser_vector_store_example[1])


