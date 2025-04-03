# 🧩 Components – OpenPages AI (Dewey-Pipeline)

This section outlines the major components of the OpenPages AI system, restructured to support a secure, modular, and AI-ready document processing pipeline. All components are CLI-first, offline-capable, and ready to be extended with NLP, vector search, or a future web UI.

---

## 🧠 CLI Command Handler

**Functionality:**

- Parses CLI flags and subcommands (e.g., `-process`, `-summary`, `-export`).
- Maps aliases or short-form flags to longer operations (e.g., `p` → `-process`).
- Controls flow between parser, classifier, and exporter modules.
- *(Future)* Integrates with an NLP parser to allow natural language flags.

**Security & UX Enhancements:**

- Only accepts PDFs from valid paths
- Supports `-dry-run` mode for safe testing

---

## 🧠 NLP Module *(Planned)*

**Functionality:**

- Translates natural language commands (e.g., “summarize my physics notes”) into CLI arguments.
- Maps phrases to internal functions in either English or Spanish.
- Enhances interaction with future web UI or CLI chatbot mode.

**Security Notes:**

- Sanitizes input phrases
- Loads only whitelisted model/tokenizers

---

## 📚 Book Logger / Metadata Tracker

**Functionality:**

- Extracts and logs metadata from PDFs: title, inferred category, Dewey code
- Stores processing history (timestamps, filenames)
- *(Optional)* Tracks document versioning or reprocessing flags

**Security Enhancements:**

- Escapes filenames to avoid path injection
- Logs user session ID (for multi-user deployments)

---

## 🗃 Local Metadata Schema

**Functionality:**

- Defines internal structure of metadata saved during processing
- Includes:
    - `title`
    - `dewey_code`
    - `category`
    - `source_filename`
    - `processed_on`

**Extensible Fields:**

- Tags, notes, language, vector ID
- Can be stored in `.json`, `.csv`, or `.sqlite`

---

## 📈 Reporting Module

**Functionality:**

- Generates terminal-based and file-based reports (summary by category, document count, etc.)
- Exportable to `.csv` or `.json`
- Localized output (EN/ES)

**Security/Integrity:**

- Validates export paths
- Ensures consistent encoding for compatibility

---

## 💾 Data Management Module

**Functionality:**

- Manages file output logic
- Avoids overwrites unless `-force` is used
- Maintains an export log

**Extra Capabilities:**

- Backup processed metadata or outputs
- Detect if file was already processed to avoid duplicates

---

## 🌐 User Preferences

**Functionality:**

- Stores optional settings like:
    - Preferred output language
    - Formal/informal tone
    - Output style (compact, verbose)
- Read from `.env` or config file

**Security:**

- Loads only from whitelisted config paths

---

## 🧹 Data Validation Module

**Functionality:**

- Detects duplicate PDFs
- Detects malformed or empty text extraction results
- Warns of missing metadata fields

**Optional Automation:**

- Fixes common formatting issues
- Flags suspicious documents

---

## 🚨 Error Handler

**Functionality:**

- Catches and logs fatal/non-fatal errors
- Provides user-friendly CLI messages in EN/ES
- *(Future)* Integrates with logging system (e.g., `logs/error.log`)

**Security-Aware:**

- Redacts paths or API keys from output
- Triggers graceful fallback flows

---

## 👋 Onboarding Module

**Functionality:**

- First-run setup experience:
    - Intro message
    - Language selection
    - Output path configuration
- *(Future)* Can scaffold `.env` and example files

**Localization:** Fully bilingual (EN/ES)

---

## 💬 Response Generator *(for future CLI chatbot/UI)*

**Functionality:**

- Templates terminal feedback messages
- Adjusts language and tone dynamically
- Separates UI text from logic for localization

**Supported Modes:**

- Formal / Casual / Humorous responses (user-defined)

---

## 🔄 Interaction Flow Controller

**Functionality:**

- Controls interactive command sequences:
    - “What do you want to do next?”
    - “Would you like to export a summary?”
- Manages flow between components (parser → classifier → export)

**Adaptable UX:**

- Switches behavior based on user input style or config

---

## 🧪 Testing Suite

**Functionality:**

- Unit tests for all major components (parser, classifier, exporter)
- Multilingual I/O tests
- Integration tests for full flow (PDF → output)

**Best Practices:**

- Uses `pytest` or similar
- Stored in `/tests` with fixtures and sample PDFs
- *(Future)* GitHub Actions for CI

---

## ✅ Summary

This component map transforms OpenPages AI into a future-proof pipeline for structured PDF processing. It balances:

- 🔄 Modularity
- 🔐 Security
- 🌍 Bilingual UX
- 🤖 AI extensibility

Ready for local use, future APIs, or educational deployment.
