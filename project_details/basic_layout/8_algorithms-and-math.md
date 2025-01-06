# Algorithms and Math

## 1. Dewey Decimal Parsing Algorithm
**Objective:** Extract and validate Dewey Decimal numbers, categories, and book titles from user input.

**Steps:**
1. Split the user input by the delimiter `-`.
2. Trim whitespace from each part.
3. Validate that the first part starts with `B.` and contains a valid Dewey Decimal number.
4. Return the parsed Dewey Decimal number, category, and title.

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

## 2. Categorization Algorithm
**Objective:** Automatically categorize books based on predefined Dewey Decimal ranges.

**Steps:**
1. Define ranges for common categories (e.g., Mathematics, Operating Systems).
2. Check where the Dewey Decimal number falls and assign the appropriate category.

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

## 3. Summary Report Algorithm
**Objective:** Generate a summary report of books by category.

**Steps:**
1. Query the database for all book entries.
2. Group books by category.
3. Count the number of books in each category.
4. Format the report in the user's preferred language.

**Pseudo-code:**
```python
function generate_summary_report(language):
    books = query_database()
    summary = group_by_category(books)
    if language == "Spanish":
        return format_summary_in_spanish(summary)
    else:
        return format_summary_in_english(summary)
```

## 4. Export Data Algorithm
**Objective:** Export the user’s data to a CSV file.

**Steps:**
1. Query the database for all book entries.
2. Write the data to a CSV file.
3. Provide a download link to the user.

**Pseudo-code:**
```python
function export_data():
    books = query_database()
    csv_file = write_to_csv(books)
    return generate_download_link(csv_file)
```

## 5. Error Handling Algorithm
**Objective:** Handle errors gracefully and provide user-friendly feedback.

**Steps:**
1. Catch errors during command execution.
2. Log the error details.
3. Respond with a friendly error message in the user’s preferred language.

**Pseudo-code:**
```python
function handle_error(error, language):
    log_error(error)
    if language == "Spanish":
        return "Ocurrió un error. Por favor, inténtalo de nuevo."
    else:
        return "An error occurred. Please try again."
```

## 6. Language Preference Algorithm
**Objective:** Adapt responses based on the user’s language preference.

**Steps:**
1. Check the user's stored language preference.
2. Format responses accordingly.

**Pseudo-code:**
```python
function respond(message, user_id):
    language = get_user_language(user_id)
    if language == "Spanish":
        return translate_to_spanish(message)
    else:
        return message
```
