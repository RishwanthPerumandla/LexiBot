from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.client import documents_collection
from app.services.validator import validate_document_clauses
from bson import ObjectId

router = APIRouter()

class ValidationRequest(BaseModel):
    document_id: str

@router.post("/validate/", tags=["Validate"])
async def validate_document(req: ValidationRequest):
    try:
        doc = documents_collection.find_one({"_id": ObjectId(req.document_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        chunks = doc.get("chunks", [])
        if not chunks:
            raise HTTPException(status_code=400, detail="No text chunks found for this document")

        validation_results = validate_document_clauses(chunks)
        return {"document_id": req.document_id, "results": validation_results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
