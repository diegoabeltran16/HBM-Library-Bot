# 📊 Algorithms and Math – OpenPages AI

This document outlines the core algorithms and logic used in the OpenPages AI (Dewey-Pipeline) system. These are implemented to support document parsing, classification, metadata enrichment, multilingual interaction, and secure export.

---

## 1. 📘 Dewey Decimal Parsing Algorithm
**Objective:** Extract and validate Dewey Decimal identifiers and metadata from user input or file metadata.

**Steps:**
1. Parse the file or input string for potential Dewey codes.
2. Ensure it matches valid numeric format (e.g., 510.0, 530.12).
3. Extract related category and title fields (if from structured input).

**Pseudo-code:**
```python
function parse_reference(input):
    parts = input.split(" - ")
    if len(parts) != 3:
        raise Error("Invalid format. Use: B. <dewey_decimal> - <category> - <title>")

    dewey_decimal = parse_dewey(parts[0])
    category = parts[1].strip()
    title = parts[2].strip()
    return dewey_decimal, category, title

function parse_dewey(part):
    if not part.startswith("B."):
        raise Error("Reference must start with 'B.'")
    decimal_number = float(part.split(" ")[1])
    return decimal_number
```

---

## 2. 🧠 Categorization Algorithm
**Objective:** Automatically assign categories based on Dewey Decimal ranges or semantic matching.

**Steps:**
1. Define ranges based on standard Dewey taxonomy.
2. Match number against ranges.
3. Return the category name.

**Example Ranges:**
- `000-099`: General works
- `500-599`: Natural sciences and mathematics
- `600-699`: Technology (applied sciences)

**Pseudo-code:**
```python
function categorize_dewey(dewey_decimal):
    if 500 <= dewey_decimal < 600:
        return "Natural sciences and mathematics"
    elif 600 <= dewey_decimal < 700:
        return "Technology"
    else:
        return "General"
```

---

## 3. 📈 Summary Report Algorithm
**Objective:** Generate a summary of document categories.

**Steps:**
1. Collect parsed metadata (from `.jsonl` or DB).
2. Group by category.
3. Count documents in each group.
4. Localize the output.

**Pseudo-code:**
```python
function generate_summary_report(language):
    books = query_metadata()
    summary = group_by_category(books)
    if language == "Spanish":
        return format_summary_in_spanish(summary)
    else:
        return format_summary_in_english(summary)
```

---

## 4. 📤 Export Data Algorithm
**Objective:** Export processed data to a CSV.

**Steps:**
1. Load all processed metadata.
2. Write to structured CSV.
3. Validate paths and encode output.

**Pseudo-code:**
```python
function export_data():
    books = query_metadata()
    csv_file = write_to_csv(books)
    return generate_export_path(csv_file)
```

---

## 5. ⚠️ Error Handling Algorithm
**Objective:** Gracefully handle runtime errors.

**Steps:**
1. Wrap key operations in try-except blocks.
2. Log full traceback for debugging.
3. Return localized user-friendly message.

**Pseudo-code:**
```python
function handle_error(error, language):
    log_error(error)
    if language == "Spanish":
        return "Ocurrió un error. Por favor, inténtalo de nuevo."
    else:
        return "An error occurred. Please try again."
```

---

## 6. 🌍 Language Preference Algorithm
**Objective:** Respond in the user’s preferred language.

**Steps:**
1. Fetch user config or `.env` language code.
2. Translate strings where needed.

**Pseudo-code:**
```python
function respond(message, user_id):
    language = get_user_language(user_id)
    if language == "Spanish":
        return translate_to_spanish(message)
    else:
        return message
```

---

## ✅ Summary
These algorithms form the cognitive and organizational backbone of OpenPages AI:
- Clear, maintainable logic
- Local-first + internationalized
- Ready for AI augmentation (embeddings, semantic matching)
- Secure and robust across environments

