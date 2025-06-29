from db.database import get_connection
from models.habit import Habit, Frequency
from datetime import datetime


def insert_habit(habit: Habit):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO habits (title, description, frequency, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            habit.title,
            habit.description,
            habit.frequency.value,
            habit.created_at.isoformat()
        ))
        conn.commit()
        return cursor.lastrowid


def get_habit_by_id(id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM habits WHERE id = ?", (id,))
        row = cursor.fetchone()
        return _row_to_habit(row) if row else None


def get_all_habits():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM habits")
        rows = cursor.fetchall()
        return [_row_to_habit(row) for row in rows]
    

def get_habits_by_frequency(frequency: Frequency):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM habits WHERE frequency=?", (frequency.value,))
        rows = cursor.fetchall()
        return [_row_to_habit(row) for row in rows]


def update_habit(id: int, habit: Habit):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE habits SET title=?, description=?, frequency=?, created_at=?
            WHERE id=?
        """, (
            habit.title,
            habit.description,
            habit.frequency.value,
            habit.created_at.isoformat(),
            id
        ))
        conn.commit()
        return cursor.rowcount > 0


def delete_habit(id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM habits WHERE id = ?", (id,))
        conn.commit()
        return cursor.rowcount > 0

def delete_all_habits():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM habits")
        conn.commit()

def _row_to_habit(row):
    """ Maps SQLite row to Habit object """
    return Habit(
        id=row[0],
        title=row[1],
        description=row[2],
        frequency=Frequency(row[3]),
        created_at=datetime.fromisoformat(row[4])
    )
