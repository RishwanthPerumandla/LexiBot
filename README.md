# 🧠 LexiBot – AI-Powered Legal Research & Clause Validation System

LexiBot is an open-source LLM-powered platform for legal professionals to analyze contracts, policies, and legal documents with clause-level intelligence. It supports clause extraction, validation, comparison, summarization, and natural language Q\&A using LLMs, RAG, and embedding-based search.

---

## ✅ Key Features

* 🔍 **Clause-Level Extraction & Tagging**
* ✅ **Clause Validator (NDA, Indemnity, etc.)**
* 🧠 **LLM Q\&A over Legal Documents** (RAG)
* 📄 **Document Comparison (Redline View)**
* 🧾 **Summarization of Legal Documents**
* 👥 Multi-role UI: Legal Teams, Analysts

---

## 🧱 Tech Stack

| Layer      | Tools/Frameworks                                                 |
| ---------- | ---------------------------------------------------------------- |
| LLM/RAG    | HuggingFace Transformers, LangChain, LLaMA, SentenceTransformers |
| Embeddings | `all-MiniLM-L6-v2`, `legal-bert`, etc.                           |
| Backend    | FastAPI, LangChain, Pydantic, Uvicorn                            |
| Frontend   | React.js + Tailwind/MUI                                          |
| DB         | MongoDB / PostgreSQL for metadata                                |
| File Store | Local / S3 / Supabase Buckets                                    |
| Vector DB  | FAISS / ChromaDB                                                 |
| DevOps     | Docker, GitHub Actions (CI), Railway/EC2 (deployment)            |
| MLOps      | MLflow, DVC, Jupyter, Docker                                     |

---

## 📦 Project Structure (Suggested)

```bash
lexibot/
├── backend/
│   ├── app/
│   │   ├── api/                   # FastAPI routers (upload, ask, validate, summarize, etc.)
│   │   ├── core/                  # Settings, config loading, constants
│   │   ├── services/              # Business logic for clause tagging, validation, RAG, etc.
│   │   ├── ml/                    # ML-specific functions (inference utils, pipelines, etc.)
│   │   ├── models/                # Pydantic schemas + DB models
│   │   ├── db/                    # DB connection, models, and ORM utils (MongoDB/Postgres)
│   │   ├── vectorstore/           # FAISS/ChromaDB integrations
│   │   ├── utils/                 # Helper functions (parsers, chunkers, logging)
│   │   └── main.py                # FastAPI entrypoint
│   ├── pipelines/
│   │   ├── clause_tagging/        # Fine-tuning scripts, label schema, training utils
│   │   ├── embeddings/            # Embedding generator scripts for text/doc chunks
│   │   ├── summarization/         # Training, testing summarization models
│   │   └── rag_pipeline/          # End-to-end RAG orchestration and testing
│   ├── tests/                     # Unit & integration tests
│   ├── Dockerfile
│   └── requirements.txt
│
├── mlops/
│   ├── mlflow/                    # MLflow experiments and setup
│   ├── dvc/                       # DVC pipelines and tracked datasets
│   ├── configs/                   # Model configs, hyperparams, TOML/YAML formats
│   └── notebooks/                 # Jupyter notebooks for experiments & prototyping
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/              # API integrations
│   │   ├── context/               # Auth & global state
│   │   └── utils/                 # File parser, highlighters, etc.
│   ├── public/
│   └── vite.config.js
│
├── deployments/
│   ├── docker-compose.yml         # For local testing with services
│   ├── ec2/                       # EC2 provisioning scripts & AMI setup
│   ├── railway/                   # Railway deployment configs
│   └── github-actions/            # CI/CD workflows for backend, frontend, and ML models
│
├── data/
│   ├── raw/                       # Uploaded or collected files
│   ├── processed/                 # Preprocessed clause chunks, summaries, etc.
│   ├── legal_templates/           # Clause templates, JSON/MD format
│   └── embeddings/                # Saved embedding vectors
│
├── vector_store/                 # Chroma/FAISS local storage
├── scripts/                      # Utility scripts (DB seeding, migrations, monitoring)
└── README.md
```

---

## 🛡️ Progress So Far (Milestone 1)

We have successfully implemented the foundational components for LexiBot's backend, document parsing, vector database setup, and RAG-based semantic Q&A.

### ✅ Project Setup

* Initialized Git repo with `.gitignore` and proper folder structure
* Set up FastAPI backend with modular architecture (`api`, `utils`, `vectorstore`, `db`)
* Added all required packages to `requirements.txt`
* Created reusable utility modules for parsing, embedding, chunking, and summarization

### ✅ Document Upload & Parsing

* `/upload` API to accept `.pdf` and `.docx` legal documents
* Parsed PDFs using `pdfminer.six` and DOCX using `python-docx`
* Stored uploaded documents in `data/raw/` and extracted plain text
* Inserted metadata and full text into MongoDB

### ✅ Text Chunking

* Implemented `chunk_text()` utility with overlap for semantic continuity
* Split long text into ~300 token chunks with 50 token overlap
* Stored chunks in MongoDB and used them for embedding

### ✅ Embeddings + Vector Store (FAISS)

* Generated embeddings using `all-MiniLM-L6-v2` via `SentenceTransformers`
* Stored embeddings and corresponding text chunks in FAISS index
* Saved FAISS index and metadata to disk (`vector_store/`)

### ✅ RAG Q&A Endpoint

* `/search` API takes `document_id` + natural language `query`
* Embeds query and retrieves top-k semantically relevant chunks from FAISS
* Injects context + query into `flan-t5-base` for answer generation
* Returns clean answer and supporting chunks
* Works completely offline and model is preloaded during startup

You can test the RAG-based Q&A flow using Swagger UI (`/docs`) or any REST client like Postman or cURL.
✅ Clause Validation

* /validate route compares document chunks against a YAML-defined clause library

* Uses cosine similarity to find best matching clauses

* Tags each clause as matched or missing with matched snippet (if any)

✅ Document Summarization

* /summarize/{doc_id} route supports extractive summarization

* Splits long text into manageable segments, summarizes each with BART (facebook/bart-large-cnn)

* Dynamically adjusts max_length and min_length based on input size to improve quality

* Updates document with summary in MongoDB

## 📌 Core Modules & To-Dos

### 1. **Document Upload & Preprocessing**
- [x] Build file uploader (PDF, DOCX)
- [x] Parse documents using `pdfminer` and `python-docx`
- [x] Extract plain text and store to MongoDB
- [x] Chunk text using custom `chunk_text()` with overlap
- [x] Embed chunks with `all-MiniLM-L6-v2` and store in FAISS
- [x] Save associated metadata (filename, time, chunks, summary)

### 2. **Clause Extraction & Tagging**
- [x] Define clause categories (e.g., NDA, indemnity, jurisdiction)
- [x] Implement clause tagging via zero-shot LLMs or fine-tuned models
- [x] Highlight tagged clauses and send to frontend via API

### 3. **Clause Validator (MiniBot)**
- [x] Build a clause template repository (JSON/Markdown)
- [x] Create validation logic to compare uploaded clauses to templates
- [x] Detect missing/modified clauses (e.g., missing NDA)
- [x] Build route to validate a document or compare two documents

### 4. **RAG-based Q&A Module**
- [x] Embed query using SentenceTransformer
- [x] Search top-k similar chunks from FAISS
- [x] Inject retrieved chunks into `flan-t5-base` pipeline
- [x] Return generated answer + context
- [x] Build endpoint `/search` for document-specific QA

### 5. **Summarization Engine**
- [x] Chunk text and summarize each block using `bart-large-cnn`
- [x] Merge chunk summaries into one cohesive summary
- [x] Store summary back to MongoDB
- [x] Return summary via `/summarize` endpoint

### 6. **Frontend UI**
- [ ] Upload form with drag-drop for legal docs
- [ ] Document detail view with metadata, text, and summary
- [ ] Highlight clause tags inside the viewer
- [ ] Q&A interface using RAG backend
- [ ] View clause validation results and redline diffs

### 7. **User Roles & Auth (Optional)**
- [ ] Create roles: Admin, Lawyer, Reviewer
- [ ] Implement RBAC via Supabase/Auth0
- [ ] Show/hide views and actions based on role

### 8. **DevOps & CI/CD**
- [ ] Dockerize FastAPI backend and React frontend
- [ ] Add GitHub Actions to lint/test backend
- [ ] Deploy to Railway/EC2 with FAISS + MongoDB
- [ ] Auto-pull docs from bucket to vector store on boot (optional)

---

## 📚 Sample Open-Source Models to Use

| Use Case         | Model Name                                  | Source       |
| ---------------- | ------------------------------------------- | ------------ |
| Embedding        | `all-MiniLM-L6-v2`, `legal-bert`            | Hugging Face |
| Summarization    | `facebook/bart-large-cnn`, `google/pegasus` | Hugging Face |
| RAG LLM          | LLaMA 2 / Mistral / Phi-2                   | Hugging Face |
| Clause Detection | Zero-shot via `facebook/bart-large-mnli`    | Hugging Face |

---

## 🛠️ Future Ideas

* AI Chat Assistant for reviewing new contracts
* Integration with Gmail/Outlook to ingest contracts
* Contract Risk Scoring (based on missing clauses)
* Multi-language legal doc support
