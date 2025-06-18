# backend/app/vectorstore/vectorsearcher.py

import faiss
import numpy as np
from pathlib import Path
import pickle

# Paths
VECTOR_INDEX_PATH = Path("vector_store/index.faiss")
METADATA_PATH = Path("vector_store/metadata.pkl")

def save_faiss_index(index, metadata):
    VECTOR_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(VECTOR_INDEX_PATH))
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

def load_faiss_index():
    if VECTOR_INDEX_PATH.exists() and METADATA_PATH.exists():
        index = faiss.read_index(str(VECTOR_INDEX_PATH))
        with open(METADATA_PATH, "rb") as f:
            metadata = pickle.load(f)
        return index, metadata
    else:
        return None, []

def search_index(query_vector, top_k=5):
    index, metadata = load_faiss_index()
    if index is None:
        return []
    D, I = index.search(query_vector, top_k)
    return [metadata[i] for i in I[0]]
