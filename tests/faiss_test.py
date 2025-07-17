import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from services.ai_service import AIService
from services.document_service import DocumentService

document_path = "F:/PSE/arcai/papers/Automatic_Visual_Detection_of_Fresh_Poultry_Egg_Quality_Inspection_using_Image_Processing.pdf"
ai_service = AIService()
document_service = DocumentService()

text_chunks = document_service.get_text_chunks(document_path=document_path)
vector_store = ai_service.get_vector_store(text_chunks=text_chunks, embedding_path="tests/embeddings")
loaded_vs = ai_service.load_vector_store_from_path(embedding_path="tests/embeddings")
print(vector_store)
print(loaded_vs)