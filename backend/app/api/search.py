from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.utils.embedding import embed_query, model as embedding_model
from app.db.client import documents_collection
from app.vectorstore.vectorstore import load_faiss_index
from transformers import pipeline

router = APIRouter(prefix="/search", tags=["Search"])

# Load Q&A pipeline
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")

class SearchRequest(BaseModel):
    query: str
    document_id: str = None  # Optional


@router.post("/")
def search_documents(payload: SearchRequest):
    query = payload.query.strip()
    document_id = payload.document_id

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Embed the query
    query_vector = embed_query(query).astype("float32").reshape(1, -1)

    # === Document-specific Search ===
    if document_id:
        try:
            doc = documents_collection.find_one({"_id": ObjectId(document_id)})
            if not doc:
                raise HTTPException(status_code=404, detail="Document not found.")
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid document ID.")

        chunks = doc.get("chunks", [])
        if not chunks:
            raise HTTPException(status_code=400, detail="No chunks available in document.")

        chunk_embeddings = embedding_model.encode(chunks, convert_to_numpy=True)
        scores = cosine_similarity(query_vector, chunk_embeddings)[0]
        top_k = min(5, len(scores))
        top_indices = scores.argsort()[::-1][:top_k]
        matched_chunks = [chunks[i] for i in top_indices]

    # === Global FAISS Search ===
    else:
        index, metadata = load_faiss_index()
        if index is None:
            raise HTTPException(status_code=404, detail="Global index not found.")

        D, I = index.search(query_vector, k=5)
        matched_chunks = [metadata[i] for i in I[0]]

    # === Improved Prompt Formatting ===
    context = "\n".join(matched_chunks)
    prompt = f"""
You are a helpful legal assistant. Based only on the context below, answer the user's question concisely and factually.
If the answer is not present in the context, say "Not mentioned in the document."

Context:
{context}

Question: {query}
Answer:""".strip()

    response = qa_pipeline(prompt, max_length=256, do_sample=False)
    answer = response[0]["generated_text"].strip()

    return {
        "query": query,
        "matched_chunks": matched_chunks,
        "answer": answer
    }
