import sqlite3
import os
from datetime import datetime

# Path to the SQLite database file
database_path = 'C:/Users/diego_dx9e5pi/OneDrive/Biblioteca - Library/references.db'


def initialize_database():
    """
    Initializes the database by creating the references table if it does not exist.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS "references" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        reference_type TEXT NOT NULL,
        identifier TEXT NOT NULL,
        title TEXT NOT NULL,
        authors TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

    conn.commit()
    conn.close()


def insert_reference(user_id, reference_type, identifier, title, authors):
    """
    Inserts a new reference into the database.

    Parameters:
    - user_id (str): Discord user ID who added the reference.
    - reference_type (str): Type of the reference (e.g., B for Book).
    - identifier (str): Dewey Decimal number or another identifier.
    - title (str): Title of the reference.
    - authors (str): Author(s) of the reference.

    Returns:
    - str: Success message or error message.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Use double quotes around the table name to avoid SQL syntax errors
        cursor.execute('''
            INSERT INTO "references" (user_id, reference_type, identifier, title, authors)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, reference_type, identifier, title, authors))

        conn.commit()
        conn.close()

        return f"Reference '{title}' added successfully."

    except sqlite3.Error as e:
        return f"Database error: {e}"


def fetch_references(query_params=None):
    """
    Fetches references from the database based on optional query parameters.

    Parameters:
    - query_params (dict, optional): Dictionary containing filter criteria.

    Returns:
    - list of tuples: Matching references.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    base_query = 'SELECT id, user_id, reference_type, identifier, title, authors, created_at FROM "references"'
    conditions = []
    values = []

    if query_params:
        for key, value in query_params.items():
            conditions.append(f"{key} = ?")
            values.append(value)

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    cursor.execute(base_query, values)
    results = cursor.fetchall()

    conn.close()
    return results


def update_reference(reference_id, update_fields):
    """
    Updates fields of an existing reference based on its ID.

    Parameters:
    - reference_id (int): ID of the reference to update.
    - update_fields (dict): Dictionary containing fields to update.

    Returns:
    - str: Success message or error message.
    """
    if not update_fields:
        return "No fields to update."

    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        set_clause = ", ".join([f"{key} = ?" for key in update_fields.keys()])
        values = list(update_fields.values()) + [reference_id]

        cursor.execute(f'''
            UPDATE "references"
            SET {set_clause}
            WHERE id = ?
        ''', values)

        conn.commit()
        conn.close()

        return f"Reference with ID {reference_id} updated successfully."

    except sqlite3.Error as e:
        return f"Database error: {e}"


def delete_reference(reference_id):
    """
    Deletes a reference from the database based on its ID.

    Parameters:
    - reference_id (int): ID of the reference to delete.

    Returns:
    - str: Success message or error message.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM "references"
            WHERE id = ?
        ''', (reference_id,))

        conn.commit()
        conn.close()

        return f"Reference with ID {reference_id} deleted successfully."

    except sqlite3.Error as e:
        return f"Database error: {e}"
