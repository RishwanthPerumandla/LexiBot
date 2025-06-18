# app/api/ask.py:
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.embedding import model as embedding_model
from app.vectorstore.vectorstore import load_faiss_index
from langchain_huggingface import HuggingFacePipeline
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document
from transformers import pipeline
import numpy as np

router = APIRouter(prefix="/ask", tags=["Q&A"])

class QuestionInput(BaseModel):
    question: str

# Load local LLM once
pipe = pipeline("text2text-generation", model="google/flan-t5-small")
llm = HuggingFacePipeline(pipeline=pipe)

@router.post("/")
def ask_question(payload: QuestionInput):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Load FAISS index + metadata
    index, metadata = load_faiss_index()
    if index is None or not metadata:
        raise HTTPException(status_code=400, detail="No indexed documents found.")

    # Embed user question
    question_embedding = embedding_model.encode([question])

    # Search similar chunks
    k = 5
    D, I = index.search(np.array(question_embedding), k)
    matched_chunks = [metadata[i] for i in I[0]]

    # Prepare LangChain docs
    docs = [Document(page_content=chunk) for chunk in matched_chunks]

    # Run QA chain
    chain = load_qa_chain(llm, chain_type="stuff")
    answer = chain.run(input_documents=docs, question=question)

    return {
        "question": question,
        "answer": answer,
        "context_snippets": matched_chunks
    }
