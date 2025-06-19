from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from app.db.client import documents_collection
from app.utils.summarizer import summarize_text

router = APIRouter(prefix="/summarize", tags=["Summarization"])

class SummarizeRequest(BaseModel):
    text: str

@router.post("/")
def summarize_input_text(req: SummarizeRequest):
    summary = summarize_text(req.text)
    return {"summary": summary}

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

    # Save summary in DB
    documents_collection.update_one(
        {"_id": ObjectId(doc_id)},
        {"$set": {"summary": summary}}
    )

    return {
        "summary": summary,
        "document_id": str(doc["_id"]),
        "filename": doc["filename"]
    }
