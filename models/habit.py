from enum import Enum
from typing import List, Optional
from datetime import datetime


class Frequency(Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    BIWEEKLY = 'biweekly'
    MONTHLY = 'monthly'


class Habit:
    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        frequency: Frequency,
        created_at: datetime,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.frequency = frequency
        self.created_at = created_at
        self.completions: List[datetime] = []
        self.streak: int = 0

    def complete(self, timestamp: Optional[datetime] = None):
        timestamp = timestamp or datetime.now()
        self.completions.append(timestamp)
        print(f"Habit '{self.title}' completed at {timestamp}.")

    def last_completed(self) -> Optional[datetime]:
        return self.completions[-1] if self.completions else None

    def __repr__(self):
        return f"Habit {self.id}: {self.title}, Frequency: {self.frequency.value}, Description: {self.description}"
