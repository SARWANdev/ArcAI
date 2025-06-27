import numpy as np

from database.utils.db_setup import database_connection
from typing import List, Optional


class DocumentService:
    def __init__(self):


    def add_document(self, project_id: int, name: str, path: str,
                     embeddings: np.ndarray, text_chunks: List[str],
                     note: Optional[str] = None) -> int:
        """
        Add a document to both MySQL and FAISS databases.

        Returns:
            document_id of the created document
        """
        # Add to MySQL
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                           INSERT INTO Document
                               (project_id, name, path, note)
                           VALUES (%s, %s, %s, %s)
                           """, (project_id, name, path, note))
            document_id = cursor.lastrowid
            connection.commit()

        # Add to FAISS
        num_chunks = self.faiss.add_embeddings(document_id, embeddings, text_chunks)

        return document_id

    def search_documents(self, query_embedding: np.ndarray, k: int = 5):
        """
        Search across all document chunks.
        """
        results = self.faiss.search(query_embedding, k)

        # You can enhance this with MySQL data if needed
        with database_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            doc_ids = {str(r['document_id']) for r in results}
            if doc_ids:
                cursor.execute(f"""
                    SELECT document_id, name, path FROM Document
                    WHERE document_id IN ({','.join(doc_ids)})
                """)
                doc_info = {str(row['document_id']): row for row in cursor}

                # Add document info to results
                for result in results:
                    result.update(doc_info.get(str(result['document_id']), {}))

        return results

    def delete_document(self, document_id: int):
        """
        Delete a document from both databases.
        """
        # Delete from FAISS first
        self.faiss.delete_document_chunks(document_id)

        # Delete from MySQL
        with database_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Document WHERE document_id = %s", (document_id,))
            connection.commit()