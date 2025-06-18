# app/utils/embedding.py:
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

# Load once at module level
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_chunks(chunks: List[str]) -> np.ndarray:
    """
    Generate embeddings for a list of text chunks.
    """
    return model.encode(chunks, convert_to_numpy=True)

def embed_query(query: str) -> np.ndarray:
    """
    Generate embedding for a single query.
    """
    return model.encode([query], convert_to_numpy=True)[0]

def embed_text(text: str) -> np.ndarray:
    """
    Alias for embed_query for compatibility.
    """
    return embed_query(text)
