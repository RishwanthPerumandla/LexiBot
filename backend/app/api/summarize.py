# app/api/summarize.py:
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from bson import ObjectId
from app.db.client import documents_collection
from app.utils.summarizer import summarize_text
router = APIRouter(prefix="/summarize", tags=["Summarization"])

# Load summarizer once (you can replace with T5 if preferred)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

class SummarizeRequest(BaseModel):
    text: str

@router.post("/")
def summarize_text(payload: str) -> str:
    if not payload or len(payload.strip()) < 100:
        raise ValueError("Text too short to summarize.")

    # 400-word chunks (approx ~512 tokens)
    sentences = payload.split(". ")
    chunks = ['. '.join(sentences[i:i+15]) for i in range(0, len(sentences), 15)]

    all_summaries = []
    for chunk in chunks:
        try:
            summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
            all_summaries.append(summary)
        except Exception as e:
            print(f"Skipping chunk due to error: {e}")
            continue

    final_summary = ' '.join(all_summaries)
    if not final_summary:
        raise ValueError("Summarization failed: no valid summaries generated.")
    
    return final_summary



@router.post("/{doc_id}")
def summarize_document(doc_id: str):
    try:
        doc = documents_collection.find_one({"_id": ObjectId(doc_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid document ID")

    text = doc.get("text", "")
    if not text or len(text.split()) < 50:
        raise HTTPException(status_code=400, detail="Text too short to summarize")

    summary = summarize_text(text)

    # Update document record with summary
    documents_collection.update_one(
        {"_id": ObjectId(doc_id)},
        {"$set": {"summary": summary}}
    )

    return {
        "summary": summary,
        "document_id": str(doc["_id"]),
        "filename": doc["filename"]
    }
