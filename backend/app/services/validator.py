from typing import List, Dict
import numpy as np
from app.utils.embedding import embed_query, embed_chunks
from app.utils.template_loader import load_clause_templates
from sklearn.metrics.pairwise import cosine_similarity

SIMILARITY_THRESHOLD = 0.45  # tune this based on empirical results

def validate_document_clauses(chunks: List[str]) -> List[Dict]:
    """
    Compares document chunks with known clause templates and reports match status.
    """
    templates = load_clause_templates()
    chunk_embeddings = embed_chunks(chunks)

    results = []

    for clause_name, template_text in templates.items():
        template_vec = embed_query(template_text).reshape(1, -1)
        sims = cosine_similarity(template_vec, chunk_embeddings)[0]
        best_idx = np.argmax(sims)
        best_score = sims[best_idx]

        if best_score >= SIMILARITY_THRESHOLD:
            results.append({
                "clause": clause_name,
                "status": "matched",
                "similarity": round(float(best_score), 3),
                "matched_chunk": chunks[best_idx]
            })
        else:
            results.append({
                "clause": clause_name,
                "status": "missing",
                "similarity": round(float(best_score), 3),
                "matched_chunk": None
            })

    return results
