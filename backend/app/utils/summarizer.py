from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str) -> str:
    if not text or len(text.strip()) < 100:
        return "Text too short to summarize."

    # Split into ~400-word chunks
    sentences = text.split(". ")
    chunks = ['. '.join(sentences[i:i+15]) for i in range(0, len(sentences), 15)]

    all_summaries = []
    for chunk in chunks:
        try:
            input_len = len(chunk.split())
            # Ensure max_length is shorter than input, but not too short
            max_len = max(30, int(0.6 * input_len))
            min_len = max(20, int(0.3 * input_len))

            summary = summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text']
            all_summaries.append(summary)
        except Exception as e:
            print(f"Skipping chunk due to error: {e}")
            continue

    final_summary = ' '.join(all_summaries)
    return final_summary or "Summarization failed."
