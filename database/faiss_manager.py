import faiss
import numpy as np
import pickle
from pathlib import Path
from .utils.configuration import FAISS_CONFIG
import os


class FaissManager:
    def __init__(self):
        self.index = None
        self.dimension = FAISS_CONFIG['embedding_dimension']
        self.index_file = Path(FAISS_CONFIG['faiss_index_path'])
        self.mapping_file = Path(FAISS_CONFIG['faiss_mapping_path'])
        self.chunk_size = FAISS_CONFIG['faiss_chunk_size']
        self._ensure_data_directory()

    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        self.index_file.parent.mkdir(parents=True, exist_ok=True)

    def initialize_index(self):
        """Initialize a new FAISS index."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.mapping = {}  # {chunk_id: (document_id, chunk_num)}
        self.next_chunk_id = 0

    def load_index(self):
        """Load existing index from disk."""
        if self.index_file.exists():
            self.index = faiss.read_index(str(self.index_file))
            with open(self.mapping_file, 'rb') as f:
                self.mapping = pickle.load(f)
            self.next_chunk_id = max(self.mapping.keys()) + 1 if self.mapping else 0
        else:
            self.initialize_index()

    def save_index(self):
        """Save the current index to disk."""
        if self.index is not None:
            faiss.write_index(self.index, str(self.index_file))
            with open(self.mapping_file, 'wb') as f:
                pickle.dump(self.mapping, f)

    def add_embeddings(self, document_id: int, embeddings: np.ndarray, text_chunks: list[str]):
        """
        Add embeddings to the FAISS index.

        Args:
            document_id: ID of the document in MySQL
            embeddings: numpy array of shape (num_chunks, dimension)
            text_chunks: list of text chunks corresponding to embeddings
        """
        if self.index is None:
            self.load_index()

        # Add embeddings to index
        start_id = self.next_chunk_id
        end_id = start_id + len(embeddings)
        self.index.add(embeddings)

        # Update mapping
        for i, (embedding, text) in enumerate(zip(embeddings, text_chunks)):
            chunk_id = start_id + i
            self.mapping[chunk_id] = {
                'document_id': document_id,
                'chunk_num': i,
                'text': text,
                'embedding': embedding  # Optional: store embedding if needed
            }

        self.next_chunk_id = end_id
        self.save_index()
        return end_id - start_id  # Return number of chunks added

    def search(self, query_embedding: np.ndarray, k: int = 5):
        """
        Search for similar chunks in the index.

        Args:
            query_embedding: numpy array of shape (dimension,)
            k: number of results to return

        Returns:
            List of tuples (score, chunk_info)
        """
        if self.index is None:
            self.load_index()

        query_embedding = query_embedding.reshape(1, -1)
        distances, indices = self.index.search(query_embedding, k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx in self.mapping:
                chunk_info = self.mapping[idx].copy()
                chunk_info['score'] = float(dist)
                results.append(chunk_info)

        return results

    def delete_document_chunks(self, document_id: int):
        """
        Remove all chunks associated with a document.
        """
        if self.index is None:
            self.load_index()

        # Find all chunk IDs for this document
        to_remove = [chunk_id for chunk_id, info in self.mapping.items()
                     if info['document_id'] == document_id]

        if not to_remove:
            return

        # Remove from index (FAISS doesn't support direct removal, so we need to rebuild)
        all_ids = np.arange(self.index.ntotal)
        keep_ids = [i for i in all_ids if i not in to_remove]

        if len(keep_ids) > 0:
            # Rebuild index with remaining vectors
            new_index = faiss.IndexFlatL2(self.dimension)
            new_index.add(self.index.reconstruct_batch(keep_ids))
            self.index = new_index
        else:
            self.initialize_index()

        # Update mapping
        for chunk_id in to_remove:
            del self.mapping[chunk_id]

        self.save_index()