# 📘 OpenPages AI – PDF Knowledge Pipeline

## 🧠 Objective

This project aims to create a simple, modular tool that automates the extraction, categorization, and formatting of scientific or technical documents in PDF format. It is designed to prepare documents for downstream tasks like semantic search, fine-tuning, and knowledge indexing.

Ideal for personal knowledge organization, educational access, and showcasing full-stack skills in AI prep, NLP, and structured pipelines.

---

## 🔧 Project Scope

The PDF Knowledge Pipeline will provide the following key functionalities:

1. **Automated PDF Processing**
    - The user places one or more PDF files in the `/input` folder.
    - The tool automatically extracts the text, processes it, and saves `.txt`, `.md`, and `.jsonl` files to the `/output` folder.
2. **Category and Dewey Suggestion**
    - The tool parses text to suggest a general category and Dewey Decimal classification (e.g., AI → 006.3, Quantum Physics → 530.12).
    - Currently based on keyword heuristics with plans for NLP-based classification.
3. **Structured Output Generation**
    - Full text is saved as plain `.txt`.
    - Markdown files include titles and clean formatting.
    - JSONL files split the content into semantic chunks, ready for use in LLM embeddings, RAG, or search systems.
4. **Offline and Open by Design**
    - No cloud services or API keys are required.
    - Runs locally, ensuring user privacy and simplicity.
5. **Optional Database Integration (Future)**
    - Output can be indexed in a local or remote database for personal knowledge search.
    - Metadata such as filename, Dewey code, and category can be logged.

---

## 🛠 Technologies Used

- **Language:** Python 3.8+
- **PDF Processing:** `PyMuPDF` (`fitz`)
- **Output Formats:** `.txt`, `.md`, `.jsonl`
- **Licensing:** Apache 2.0
- **Version Control:** GitHub

---

## 💡 Future Enhancements (Optional)

- **AI-Powered Classification:** Use spaCy, OpenAI, or local LLMs to detect more accurate categories.
- **PDF Metadata Parsing:** Extract DOI, author, year, and use them as context fields.
- **Custom Chunking Logic:** Allow chunking by section headers, page breaks, or semantic blocks.
- **Embedding Generator:** Auto-generate vector embeddings and store them using FAISS or Weaviate.
- **Web Interface:** Add a simple drag-and-drop interface for PDF upload and output preview.
- **Dewey Training Set:** Fine-tune a classifier model on Dewey-tagged texts for better automation.

---

## ✅ Getting Started

1. Clone the repo and install dependencies:
    
    ```bash
    bash
    CopyEdit
    pip install pymupdf
    
    ```
    
2. Add PDFs to the `/input` folder.
3. Run the script:
    
    ```bash
    bash
    CopyEdit
    python main.py
    
    ```
    
4. Check the `/output` folder for:
    - `document.txt`
    - `document.md`
    - `document.jsonl`

---
