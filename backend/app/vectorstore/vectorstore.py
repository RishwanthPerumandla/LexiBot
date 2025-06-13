import faiss
import numpy as np
from pathlib import Path
import pickle

# Set file paths
VECTOR_INDEX_PATH = Path("vector_store/index.faiss")
METADATA_PATH = Path("vector_store/metadata.pkl")

def save_faiss_index(index, metadata):
    VECTOR_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(VECTOR_INDEX_PATH))
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

def load_faiss_index():
    if VECTOR_INDEX_PATH.exists():
        index = faiss.read_index(str(VECTOR_INDEX_PATH))
        with open(METADATA_PATH, "rb") as f:
            metadata = pickle.load(f)
        return index, metadata
    else:
        return None, []

def create_and_store_index(embeddings, chunks):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Store full text chunks as metadata for retrieval
    metadata = chunks
    save_faiss_index(index, metadata)
    return index
