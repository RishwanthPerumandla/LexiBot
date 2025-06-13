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
| MLOps      | MLflow, DVC, Jupyter, Docker |


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
│   │   └── utils/                 # Helper functions (parsers, chunkers, logging)
│   ├── pipelines/
│   │   ├── clause_tagging/        # Fine-tuning scripts, label schema, training utils
│   │   ├── embeddings/            # Embedding generator scripts for text/doc chunks
│   │   ├── summarization/         # Training, testing summarization models
│   │   └── rag_pipeline/          # End-to-end RAG orchestration and testing
│   ├── tests/                     # Unit & integration tests
│   ├── main.py                    # FastAPI entrypoint
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
│   └── github-actions/           # CI/CD workflows for backend, frontend, and ML models
│
├── data/
│   ├── raw/                       # Uploaded or collected files
│   ├── processed/                 # Preprocessed clause chunks, summaries, etc.
│   ├── legal_templates/          # Clause templates, JSON/MD format
│   └── embeddings/               # Saved embedding vectors
│
├── vector_store/                 # Chroma/FAISS local storage
├── scripts/                      # Utility scripts (DB seeding, migrations, monitoring)
└── README.md

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
