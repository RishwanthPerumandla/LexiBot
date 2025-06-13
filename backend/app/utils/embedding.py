from typing import List
from sentence_transformers import SentenceTransformer

# Load once at module level
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of text chunks.
    """
    embeddings = model.encode(chunks, convert_to_numpy=True)
    return embeddings
