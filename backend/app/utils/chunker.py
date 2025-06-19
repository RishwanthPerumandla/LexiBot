# app/utils/chunker.py:
from typing import List

def chunk_text(
    text: str,
    max_tokens: int = 300,
    overlap: int = 50
) -> List[str]:
    """
    Splits the input text into chunks of max_tokens size with optional overlap.
    """
    import re

    # Basic sentence splitting (you can replace with nltk or spacy for smarter logic)
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = []
    current_len = 0

    for sentence in sentences:
        word_count = len(sentence.split())

        if current_len + word_count > max_tokens:
            chunks.append(" ".join(current_chunk))
            # Start new chunk with overlap from previous
            overlap_tokens = current_chunk[-overlap:] if overlap < len(current_chunk) else current_chunk
            current_chunk = overlap_tokens + sentence.split()
            current_len = len(current_chunk)
        else:
            current_chunk += sentence.split()
            current_len += word_count

    # Add last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
