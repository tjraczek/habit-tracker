from db.database import get_connection
from datetime import datetime
from typing import List


def complete_habit(habit_id: int, timestamp: datetime = None):
    timestamp = timestamp or datetime.now()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO habit_completions (habit_id, completed_at)
        VALUES (?, ?)
        """, (habit_id, timestamp.isoformat()))
        conn.commit()


def get_completions(habit_id: int) -> List[datetime]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT completed_at FROM habit_completions
        WHERE habit_id = ?
        ORDER BY completed_at ASC
        """, (habit_id,))
        rows = cursor.fetchall()
        return [datetime.fromisoformat(row[0]) for row in rows]
