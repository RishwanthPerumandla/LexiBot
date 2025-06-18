from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.embedding import embed_text
from app.vectorstore.vectorsearcher import load_faiss_index
import numpy as np

router = APIRouter(prefix="/search", tags=["Search"])

class SearchQuery(BaseModel):
    query: str
    top_k: int = 3

@router.post("/")
def semantic_search(query: SearchQuery):
    # Validate
    if not query.query or len(query.query.strip()) < 5:
        raise HTTPException(status_code=400, detail="Query too short.")

    # Load vector index and metadata
    index, metadata = load_faiss_index()
    if index is None:
        raise HTTPException(status_code=500, detail="Vector index not found.")

    # Embed the query
    query_vec = embed_text(query.query).reshape(1, -1)

    # Perform similarity search
    D, I = index.search(query_vec, query.top_k)
    
    results = []
    for idx in I[0]:
        if 0 <= idx < len(metadata):
            results.append(metadata[idx])
    
    return {
        "query": query.query,
        "results": results
    }
