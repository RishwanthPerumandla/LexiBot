# app/utils/summarizer.py:
from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text: str) -> str:
    if not text or len(text.strip()) < 100:
        return "Text too short to summarize."

    # Truncate to a safe length for BART (approx. 1024 tokens)
    text = text[:2000]

    result = summarizer(text, max_length=200, min_length=50, do_sample=False)
    return result[0]["summary_text"]
