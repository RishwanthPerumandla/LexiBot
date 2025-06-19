from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline, AutoTokenizer

from app.utils.embedding import embed_query, model as embedding_model
from app.db.client import documents_collection
from app.vectorstore.vectorstore import load_faiss_index

router = APIRouter(prefix="/search", tags=["Search"])

# Load model and tokenizer once
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

# Request schema
class SearchRequest(BaseModel):
    query: str
    document_id: str = None  # Optional


# Utility: Truncate context tokens safely
def truncate_context(text: str, max_tokens: int = 400) -> str:
    tokens = tokenizer.encode(text, truncation=True, max_length=max_tokens)
    return tokenizer.decode(tokens, skip_special_tokens=True)


# Utility: Construct prompt for legal QA
def legal_prompt(context: str, question: str) -> str:
    return (
        "You are a professional and friendly legal assistant. Based on the following context, answer the user's question in a clear and helpful tone.\n"
        "Start your response with a brief acknowledgment (e.g., “Yes, here are the details…” or “Let me check that for you…”).\n"
        "If the information is not available, say “It appears that this detail is not mentioned in the document.”\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )


@router.post("/")
def search_documents(payload: SearchRequest):
    query = payload.query.strip()
    document_id = payload.document_id

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Embed query
    query_vector = embed_query(query).astype("float32").reshape(1, -1)

    # === Document-specific search ===
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
        top_indices = scores.argsort()[::-1][:min(5, len(scores))]
        matched_chunks = [chunks[i] for i in top_indices]

    # === Global FAISS search ===
    else:
        index, metadata = load_faiss_index()
        if index is None:
            raise HTTPException(status_code=404, detail="Global index not found.")

        D, I = index.search(query_vector, k=5)
        matched_chunks = [metadata[i] for i in I[0]]

    # === Prompt construction and model inference ===
    raw_context = "\n".join(matched_chunks)
    trimmed_context = truncate_context(raw_context)
    prompt = legal_prompt(trimmed_context, query)

    response = qa_pipeline(prompt, max_new_tokens=128, do_sample=False)
    answer = response[0]["generated_text"].strip()

    return {
        "query": query,
        "matched_chunks": matched_chunks,
        "answer": answer
    }
