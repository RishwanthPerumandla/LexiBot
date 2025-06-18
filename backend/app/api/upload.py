from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from app.utils.parser import parse_document
from app.utils.chunker import chunk_text
from app.utils.embedding import embed_chunks
from app.vectorstore.vectorstore import create_and_store_index

from app.db.client import documents_collection
from app.db.models import create_document_record



router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = Path("data/raw")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF or DOCX files are supported.")

    file_path = UPLOAD_DIR / file.filename
    contents = await file.read()
    file_path.write_bytes(contents)

    text = parse_document(file_path)
    # After parsing text
    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)
    # After extracting text and chunks:
    record = create_document_record(file.filename, text, chunks)
    documents_collection.insert_one(record)
    create_and_store_index(embeddings, chunks)


    return {
        "filename": file.filename,
        "size": len(contents),
        "num_chunks": len(chunks),
        "chunk_preview": chunks[:2]
    }