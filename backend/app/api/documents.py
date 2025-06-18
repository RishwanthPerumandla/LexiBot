# app/api/documents.py:
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.db.client import documents_collection

router = APIRouter(prefix="/documents", tags=["Documents"])

# Helper to convert ObjectId to string
def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/")
def list_documents():
    docs = list(documents_collection.find({}, {"filename": 1, "upload_time": 1}))
    return [serialize_doc(doc) for doc in docs]

@router.get("/{doc_id}")
def get_document(doc_id: str):
    try:
        doc = documents_collection.find_one({"_id": ObjectId(doc_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        return serialize_doc(doc)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid document ID")
