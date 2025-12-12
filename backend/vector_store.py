from typing import List, Dict, Tuple
from embed import embed_text, cosine_similarity


class VectorStore:
    """
    Simple in-memory vector store for semantic search using cosine similarity.
    Stores text chunks along with metadata and precomputed embeddings.
    """

    def __init__(self):
        self.documents: List[Dict] = []

    # ----------------------------------------------------------
    def add(self, text: str, metadata: Dict):
        """
        Add a text chunk + metadata to the vector store.

        Parameters:
        - text (str): Raw text to embed.
        - metadata (dict): Extra information (e.g., resume section).
        """
        embedding = embed_text(text)

        self.documents.append({
            "text": text,
            "metadata": metadata,
            "embedding": embedding,
        })

    # ----------------------------------------------------------
    def search(self, query: str, top_k: int = 3) -> List[Tuple[float, Dict]]:
        """
        Perform semantic search using cosine similarity.

        Parameters:
        - query (str): User query to embed + compare.
        - top_k (int): Number of results to return.

        Returns:
        List of tuples → (similarity_score, document_dict)
        """
        if not self.documents:
            return []

        query_vec = embed_text(query)
        scores = []

        for doc in self.documents:
            sim = cosine_similarity(query_vec, doc["embedding"])
            scores.append((sim, doc))

        # Sort by highest similarity
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:top_k]


# ----------------------------------------------------------
# Singleton instance used throughout the backend
# ----------------------------------------------------------
vector_store = VectorStore()
