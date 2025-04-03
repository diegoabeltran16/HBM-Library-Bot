# 🏗️ Architecture – OpenPages AI (Dewey-Pipeline)

OpenPages AI is designed with a clean, modular, and scalable architecture that ensures offline-first performance, knowledge transparency, and AI readiness. Below is a modernized, security-aware version of the architecture adapted from traditional bot systems to local and/or CLI-based document pipelines.

---

## 🧱 Architecture Layers

1. **User Interaction Layer**
2. **Application Logic Layer**
3. **Data Layer**
4. **Integration Layer**
5. **Security Layer (Cross-Cutting)**

---

## 🎛️ User Interaction Layer

**Description:** This layer represents how users interact with the system. In the current stage, it's CLI-based, with future support for a web interface.

**Components:**

- **CLI Commands / Scripts**
- *(Future)* Minimal Web UI (Drag & Drop)

**Responsibilities:**

- Receive and parse user input (e.g., run commands, pass flags like `-summary`, `-export`)
- Display multilingual output (EN/ES)
- Guide new users via onboarding messages

---

## 🧠 Application Logic Layer

**Description:** Core of the pipeline. Orchestrates parsing, classification, export, and feedback.

**Components:**

1. **File Scanner** – Scans `/input/` for new PDFs.
2. **PDF Parser** – Extracts text using `PyMuPDF`.
3. **Classifier** – Detects Dewey Decimal category based on content (via keyword match or embeddings).
4. **Filename Builder** – Generates output filenames using Dewey + category.
5. **Exporter** – Writes `.txt`, `.md`, `.jsonl` to `/output/`.
6. **Error Handler** – Logs and displays friendly feedback.

**Responsibilities:**

- Modular control of the processing pipeline
- Support batch processing
- Allow CLI flags and options

---

## 🗃 Data Layer

**Description:** Manages persistent and intermediate outputs. Future-ready for database or vector store integrations.

**Components:**

1. **File Storage (local):** `/input/`, `/output/`
2. **Structured Output Format:** `.jsonl`, `.md`, `.txt`
3. *(Optional)* Local SQLite DB or CSV log for summaries

**Responsibilities:**

- Store processed data in portable, AI-ready formats
- Maintain metadata logs for future querying
- Ensure consistency in output formatting and versioning

---

## 🔌 Integration Layer

**Description:** Interfaces with future external tools or services.

**Components:**

1. **Embedding Generator (OpenAI, HuggingFace)**
2. **Vector Store (FAISS, Weaviate)**
3. *(Future)* Web UI / FastAPI endpoint

**Responsibilities:**

- Export data to downstream ML/AI models
- Enable semantic search, RAG, or fine-tuning
- Accept external uploads via CLI/Web

---

## 🔐 Security Layer (Cross-Cutting Concern)

**Description:** Security and privacy are built into every part of the pipeline.

**Practices Implemented:**

### 1. **Environment-based Configuration**

- Secrets (API keys, paths) managed via `.env` file (never hardcoded)
- Example: `OPENAI_API_KEY`, `OUTPUT_DIR`

### 2. **Input Sanitization**

- Validate file types (only `.pdf` allowed)
- Escape file names and clean paths to prevent injection or traversal attacks

### 3. **Safe Output Handling**

- Overwrite protection (check if output file already exists)
- Temp folder handling (if batch crash occurs, no data loss)

### 4. **Optional HTTPS/SSL Handling (For Web/Cloud)**

- Enforce HTTPS if web interface is added
- All APIs must validate SSL certs by default

### 5. **Access Control (Future)**

- If exposed via API or UI, implement token-based access with scoped roles

### 6. **Audit Logging**

- Track which files were processed, renamed, or exported
- Useful for educational and regulatory transparency

---

## 📐 Future Architecture Enhancements

1. **CLI Framework with `argparse` or `click`**
    - Support commands like `-process`, `-export`, `-summary`, `-help`
2. **Modular Plugin System**
    - Users can drop their own `classifier.py` or `exporter.py`
3. **Web Interface (Minimal)**
    - Flask/FastAPI-based uploader with visual summary display
4. **Embeddings & Search Engine**
    - Store vectors and enable question answering across processed docs
5. **Multilingual NLP Pipeline**
    - Language detection and internationalized output formatting
6. **Dockerized Deployment**
    - One-click container for reproducibility
7. **CI/CD for Testing**
    - GitHub Actions for linting, testing, and validation on push

---

## ✅ Summary

OpenPages AI is designed to scale from a personal knowledge processor to a fully modular AI-ready tool. Its architecture ensures:

- ✨ Simplicity for beginners
- 🧠 Extensibility for developers
- 🛡️ Security and ethics for real-world use

Let’s keep it clean, open, and powerful.
