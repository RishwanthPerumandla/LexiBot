# app/db/models.py:
from typing import List
from datetime import datetime

def create_document_record(filename: str, text: str, chunks: List[str], summary: str = None):
    return {
        "filename": filename,
        "upload_time": datetime.utcnow(),
        "text": text,
        "chunks": chunks,
        "summary": summary
    }
