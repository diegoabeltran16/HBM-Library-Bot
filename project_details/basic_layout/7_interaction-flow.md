# 🤖 Interaction Flow – OpenPages AI

This document outlines how users interact with the OpenPages AI pipeline, covering onboarding, file processing, output generation, multilingual feedback, and error handling. The flow is designed to be scalable for terminal/CLI use and future web interfaces.

---

## 🪠 Initial Setup & Onboarding (Detailed)

### 👩‍💻 Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/openpages-ai.git
cd openpages-ai

```

### 🐍 Step 2: Set Up the Python Environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

```

### 📦 Step 3: Install Dependencies

```bash
pip install -r requirements.txt

```

### 📂 Step 4: Add Input Files

```bash
mkdir input output
# Place your PDF files inside /input

```

Example:

```
openpages-ai/
├── input/
│   └── Quantum_Mechanics_Notes.pdf
├── output/

```

### ▶️ Step 5: Run the Processor

```bash
python main.py

```

Terminal Output:

```
📘 Processing: Quantum_Mechanics_Notes.pdf
🚗 Saved: 530.12_Physics_Quantum_Mechanics_Notes.txt
🚗 Saved: 530.12_Physics_Quantum_Mechanics_Notes.md
🚗 Saved: 530.12_Physics_Quantum_Mechanics_Notes.jsonl
🧠 Suggested Dewey: 530.12 — Physics

```

---

## 📂 File Naming Convention (Dewey-Based)

All output files are named using the Dewey Decimal number and category, to support better organization:

**Pattern:**

```
<Dewey>_<Category>_<OriginalFileName>.<ext>

```

**Examples:**

- `530.12_Physics_Quantum_Mechanics_Notes.jsonl`
- `006.3_AI_AI_Essentials.md`

This makes sorting and retrieval much easier in large-scale knowledge bases.

**Components Involved:**`Classifier`, `Filename Builder`, `Exporter`

---

## 📄 Processing a PDF Document

**User Action:**

- Place PDF(s) in `/input/`
- Run `python main.py`

**System Response (EN):**

> ✅ Processed: AI_Essentials.pdf — Category: Artificial Intelligence, Dewey: 006.3
> 

**System Response (ES):**

> ✅ Procesado: AI_Essentials.pdf — Categoría: Inteligencia Artificial, Dewey: 006.3
> 

**Generated Files:**

- `006.3_AI_AI_Essentials.txt`
- `006.3_AI_AI_Essentials.md`
- `006.3_AI_AI_Essentials.jsonl`

**Modules:** `Parser`, `Classifier`, `Exporter`

---

## 🧠 Suggesting a Dewey Category

**Logic:**

- AI/Machine Learning: `006.3`
- Quantum Physics: `530.12`
- Mathematics: `510`

**Output Example (EN):**

> 🧠 Suggested Dewey: 510 — Mathematics
> 

**Output Example (ES):**

> 🧠 Dewey sugerido: 510 — Matemáticas
> 

**Modules:** `Classifier`, `Keyword Matching`, `Future Embedding Engine`

---

## 📈 Export Summary Report *(Future)*

**User:**

```bash
python main.py --summary

```

**Output (EN):**

> Library Summary: 3 under Mathematics, 2 under Quantum Physics.
> 

**Output (ES):**

> Resumen: 3 bajo Matemáticas, 2 bajo Física Cuántica.
> 

**Modules:** `Summary Generator`, `Database/Log Reader`

---

## 📅 Exporting Data *(Future)*

**User:**

```bash
python main.py --export --format=csv

```

**System Response:**

> 📂 Exported summary_export.csv to /output
> 

**Modules:** `Exporter`, `Report Builder`, `CLI Handler`

---

## ⚠️ Handling Errors

**Scenario:** User adds a non-PDF file to `/input/`

**Output (EN):**

> ⚠️ Error processing 'notes.txt': Invalid file format. Please use PDF.
> 

**Output (ES):**

> ⚠️ Error al procesar 'notes.txt': Formato inválido. Por favor usa PDF.
> 

**Modules:** `Error Handler`, `File Validator`

---

## 🚀 Interactive Session Example

1. **User:** Places `Calculus_Intro.pdf` into `/input/`
2. **System:**
    
    > 📘 Processing: Calculus_Intro.pdf
    > 
    > 
    > ✅ Saved: 510_Mathematics_Calculus_Intro.jsonl
    > 
3. **System:**
    
    > Would you like a summary? (Coming soon)
    > 
4. **User:** `-summary`
5. **System:**
    
    > Current breakdown: 4 docs in Mathematics, 2 in Physics
    > 

**Modules:** `Command Handler`, `Book Logger`, `Classifier`, `Exporter`

---

## 🔄 Multilingual UX

All system outputs are prepared to support both **English and Spanish**. A language preference flag or auto-detection can be added later.

| Prompt | English | Spanish |
| --- | --- | --- |
| Startup | "Ready to process your documents!" | "¡Listo para procesar tus documentos!" |
| Error | "Invalid file format." | "Formato de archivo inválido." |
| Dewey | "Suggested Dewey: 510" | "Dewey sugerido: 510" |

**Modules:** `Response Generator`, `Language Handler`

---
