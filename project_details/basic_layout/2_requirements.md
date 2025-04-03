# 📘 OpenPages AI – PDF Knowledge Pipeline

## Requirements

---

### ✅ Functional Requirements

1. The system must allow users to process PDF documents placed in a designated `/input` directory.
2. The system must extract and clean text content from PDF files.
3. The system must generate output files in three formats: `.txt`, `.md`, and `.jsonl`.
4. The system must suggest a Dewey Decimal category based on keywords in the text.
5. The output files must be stored in an `/output` directory with a consistent naming scheme.

---

### ⚙️ Non-Functional Requirements

1. The tool should complete processing of standard PDFs (under 10 pages) in less than 2 seconds.
2. The pipeline should work offline and not depend on external APIs.
3. The output formats should be clean and ready for downstream use (e.g., AI models).
4. The system should handle batch processing of multiple PDFs reliably.

---

### 💻 Software Requirements

1. Python 3.8 or higher
2. `PyMuPDF` (`pymupdf`) for PDF text extraction
3. Standard Python libraries: `os`, `json`, `re`
4. Optional: `python-dotenv` for future environment variable handling

---

### 🧑‍💻 Technical Requirements

1. Must support modular architecture (separate files for parsing, classifying, exporting).
2. Must allow for easy customization of output formats (markdown styling, chunking rules, etc.).
3. Must be easily containerizable (e.g., Docker) for scalable or cloud deployment.
4. Optional database integration for storing and querying processed document metadata.

---

### 📦 Libraries

| Library | Purpose |
| --- | --- |
| `pymupdf` | Extract structured text from PDF |
| `json` | Export data in JSONL format |
| `os` / `pathlib` | Handle file system navigation |
| `re` | Keyword matching for classification |
| (optional) `dotenv` | Manage environment variables |

---

### ✅ Testing Requirements

1. Unit tests must be written for each core function (PDF reading, classification, output generation).
2. Basic input validation and malformed PDF handling should be tested.
3. Performance benchmarks should be tracked for large document processing.
4. Manual testing must ensure clean output formatting across formats.

---

### 🧪 Quality Assurance Requirements

1. Code must follow PEP 8 standards.
2. Functions must be modular and documented using docstrings.
3. Project must include a `README.md`, `LICENSE`, and `requirements.txt`.
4. (Optional) Use GitHub Actions or similar for basic CI test pipeline.

---

### 🔐 Security Requirements

1. No external API keys should be hardcoded in the codebase.
2. If using `.env` files in the future, they must be excluded via `.gitignore`.
3. All outputs must be local unless explicitly configured for remote sync.
4. Future additions like embedding APIs should use secure connection protocols.

---

### 🚀 Technologies Used

- **Language:** Python 3.8+
- **PDF Parser:** PyMuPDF
- **Output Formats:** Plain text, Markdown, JSONL
- **Version Control:** GitHub
- **License:** Apache 2.0 (open for commercial + personal use)

---

### 🔮 Future Enhancements

- **AI Classification:** NLP-based classification instead of keyword detection
- **Database Support:** Add SQLite or Postgres support to store and search processed content
- **Embeddings Engine:** Create embeddings from chunks for use in RAG or vector search
- **Web Interface:** Add a simple frontend for drag-and-drop PDF processing
- **Multi-language Support:** Support document classification in Spanish, English, etc.

---
