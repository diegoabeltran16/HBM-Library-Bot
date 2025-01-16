import sqlite3
import os

# Path to the SQLite database file
database_path = 'C:/Users/diego_dx9e5pi/OneDrive/Biblioteca - Library/references.db'


def initialize_database():
    """
    Initializes the database by creating the references table if it does not exist.
    """
    try:
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
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()


def insert_reference(user_id, reference_type, identifier, title, authors):
    """
    Inserts a new reference into the database.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO "references" (user_id, reference_type, identifier, title, authors)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, reference_type, identifier, title, authors))

        conn.commit()
        return f"Reference '{title}' added successfully."
    except sqlite3.Error as e:
        return f"Database error: {e}"
    finally:
        conn.close()


def fetch_references(query_params=None):
    """
    Fetches references from the database based on optional query parameters.

    If `query_params` contains a "query" key, it performs a flexible search across 
    reference_type, identifier, title, and authors fields.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        base_query = 'SELECT id, user_id, reference_type, identifier, title, authors, created_at FROM "references"'
        conditions = []
        values = []

        if query_params and "query" in query_params:
            query_value = f"%{query_params['query']}%"
            conditions.append(
                "(reference_type LIKE ? OR identifier LIKE ? OR title LIKE ? OR authors LIKE ?)"
            )
            values.extend([query_value] * 4)

        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)

        cursor.execute(base_query, values)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"Error fetching references: {e}")
        return []
    finally:
        conn.close()
