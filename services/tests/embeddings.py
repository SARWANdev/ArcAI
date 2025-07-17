

from services.ai_service import AIService
from services.upload_manager.embeddings_manager import EmbeddingsManager
from services.upload_manager.server_conection import save_embeddings






vector_store_example = AIService().get_vector_store(["hola", "amigos", "como", "estan"])
print(vector_store_example)

ser_vector_store_example = EmbeddingsManager.serialize_vector_store(vector_store_example)
print(type(ser_vector_store_example))

remote_path = "/home/pse03/117530366620837166459/687263f6d6adfb6fdfa4aa4d/b873ee2ef42e2209ef03c15d13c71b5481062a97818f0dab93d69f9fb7c718ff/b873ee2ef42e2209ef03c15d13c71b5481062a97818f0dab93d69f9fb7c718ff.pdf"


save_embeddings(remote_path, ser_vector_store_example[0], ser_vector_store_example[1])

print(type(EmbeddingsManager.load_remote_faiss_index(remote_path)))


