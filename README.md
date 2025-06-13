#  LexiBot – AI-Powered Legal Research & Clause Validation System

LexiBot is an open-source LLM-powered platform for legal professionals to analyze contracts, policies, and legal documents with clause-level intelligence. It supports clause extraction, validation, comparison, summarization, and natural language Q&A using LLMs, RAG, and embedding-based search.

---

## ✅ Key Features

- 🔍 **Clause-Level Extraction & Tagging**  
- ✅ **Clause Validator (NDA, Indemnity, etc.)**
- 🧠 **LLM Q&A over Legal Documents** (RAG)
- 📄 **Document Comparison (Redline View)**
- 🧾 **Summarization of Legal Documents**
- 👥 Multi-role UI: Legal Teams, Analysts

---

## 🧱 Tech Stack

| Layer       | Tools/Frameworks |
|------------|------------------|
| LLM/RAG    | HuggingFace Transformers, LangChain, LLaMA, SentenceTransformers |
| Embeddings | `all-MiniLM-L6-v2`, `legal-bert`, etc. |
| Backend    | FastAPI, LangChain, Pydantic, Uvicorn |
| Frontend   | React.js + Tailwind/MUI |
| DB         | MongoDB / PostgreSQL for metadata |
| File Store | Local / S3 / Supabase Buckets |
| Vector DB  | FAISS / ChromaDB |
| DevOps     | Docker, GitHub Actions (CI), Railway/EC2 (deployment) |

---

## 📦 Project Structure (Suggested)

```bash
lexibot/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/   # RAG, embeddings, clause tagging, etc.
│   │   ├── models/
│   │   └── utils/
│   ├── main.py
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── public/
│   └── vite.config.js
├── data/
│   ├── legal_templates/
│   └── uploads/
└── vector_store/
```

---

## 📌 Core Modules & To-Dos

### 1. **Document Upload & Preprocessing**
- [ ] Build file uploader (PDF, DOCX)
- [ ] Parse documents → extract text using `pdfminer` or `docx2txt`
- [ ] Split into meaningful chunks (e.g., paragraphs, clauses)
- [ ] Store metadata (title, upload time, user, etc.)

### 2. **Clause Extraction & Tagging**
- [ ] Define clause categories (e.g., NDA, indemnity, jurisdiction, etc.)
- [ ] Train/finetune or use zero-shot LLMs for tagging clause types
- [ ] Highlight and label extracted clauses in frontend

### 3. **Clause Validator (MiniBot)**
- [ ] Create clause template bank (JSON or Markdown)
- [ ] Validate if document has mandatory clauses (NDA, Termination, etc.)
- [ ] Flag missing or altered clauses
- [ ] Compare against previous version (doc1 vs doc2)

### 4. **RAG-based Q&A Module**
- [ ] Embed chunks using MiniLM / LegalBERT
- [ ] Store embeddings in FAISS/Chroma
- [ ] Set up LangChain RAG pipeline with context injection
- [ ] Build FastAPI route to handle `/ask-question`

### 5. **Summarization Engine**
- [ ] Use T5 or Bart-based summarization models from HuggingFace
- [ ] Chunk long documents + summarize key sections (clauses, risks, etc.)
- [ ] Return summary with highlights to frontend

### 6. **Frontend UI**
- [ ] Dashboard for uploaded docs
- [ ] View document with clause labels + redline comparison
- [ ] Ask a Question input box (RAG)
- [ ] Summary + clause validation results

### 7. **User Roles & Auth (Optional)**
- [ ] Add role-based UI (lawyer, admin, viewer)
- [ ] Use Supabase auth / Clerk / Auth0 (free tier)

### 8. **DevOps & CI/CD**
- [ ] Dockerize backend + frontend
- [ ] Set up GitHub Actions for lint/test/build
- [ ] Deploy via Railway / Render / EC2

---

## 📚 Sample Open-Source Models to Use

| Use Case            | Model Name                                | Source         |
|---------------------|--------------------------------------------|----------------|
| Embedding           | `all-MiniLM-L6-v2`, `legal-bert`           | Hugging Face   |
| Summarization       | `facebook/bart-large-cnn`, `google/pegasus`| Hugging Face   |
| RAG LLM             | LLaMA 2 / Mistral / Phi-2                   | Hugging Face   |
| Clause Detection    | Zero-shot via `facebook/bart-large-mnli`   | Hugging Face   |

---

## 🛠️ Future Ideas

- AI Chat Assistant for reviewing new contracts
- Integration with Gmail/Outlook to ingest contracts
- Contract Risk Scoring (based on missing clauses)
- Multi-language legal doc support
