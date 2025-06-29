import sqlite3

def get_connection():
    """" connects to the local SQLite database or creates a new database file called habits.db """
    return sqlite3.connect("habits.db")

def init_db():
    """ initializes the database by creating two tables if they do not exist yet """
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            frequency TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS habit_completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_at TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
        )
        """)
        conn.commit()
