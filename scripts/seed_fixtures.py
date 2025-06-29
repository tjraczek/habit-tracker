from datetime import datetime, timedelta
from models.habit import Habit, Frequency
from db.habit_repository import insert_habit, get_all_habits
from db.habit_completion_repository import complete_habit

def create_sample_habits():
    """ Creates five sample habits with 2 daily, 1 weekly, 1 biweekly, 1 monthly. """
    habits = [
        Habit(id=0, title="Brush Teeth", description="Brush teeth every morning", frequency=Frequency.DAILY, created_at=datetime(2020, 12, 12)),
        Habit(id=0, title="Workout", description="Exercise once a week", frequency=Frequency.WEEKLY, created_at=datetime(2021, 3, 3)),
        Habit(id=0, title="Read Book", description="Read every day", frequency=Frequency.DAILY, created_at=datetime(2022, 4, 4)),
        Habit(id=0, title="Review Car", description="Check if everything works in the car", frequency=Frequency.MONTHLY, created_at=datetime.now()),
        Habit(id=0, title="Pay Rent", description="Pay rent every other week", frequency=Frequency.BIWEEKLY, created_at=datetime(2023, 1, 1)),
    ]

    for habit in habits:
        insert_habit(habit)

    print(f"{len(habits)} sample habits inserted.")


def seed_sample_completions():
    """ Populates completions with streaks. """
    habits = get_all_habits()
    print("Seeding completions...")

    for habit in habits:
        created = habit.created_at
        today = datetime.now()
        current = created

        if habit.title == "Pay Rent":
            # Special: simulate irregular biweekly streak
            completions = [
                created,
                created + timedelta(weeks=2),
                # skip week 4
                created + timedelta(weeks=6)
            ]
            for date in completions:
                complete_habit(habit.id, date)
            continue

        """ Seed daily habits, with breaks for 'Read Book' """
        skip_dates = []
        if habit.title == "Read Book":
            # Skip 2 days: day 200 and day 800 after creation date
            skip_dates = [created + timedelta(days=200), created + timedelta(days=800)]

        while current <= today:
            if habit.frequency == Frequency.DAILY:
                if current.date() == today.date():
                    current += timedelta(days=1)
                    continue
                if habit.title == "Read Book" and any(current.date() == skip.date() for skip in skip_dates):
                    current += timedelta(days=1)
                    continue
                complete_habit(habit.id, current)

            elif habit.frequency == Frequency.WEEKLY:
                if current.weekday() == created.weekday():
                    complete_habit(habit.id, current)

            elif habit.frequency == Frequency.BIWEEKLY:
                delta_days = (current - created).days
                if delta_days % 14 == 0:
                    complete_habit(habit.id, current)

            elif habit.frequency == Frequency.MONTHLY:
                if current.day == created.day:
                    complete_habit(habit.id, current)

            current += timedelta(days=1)

    print("Completion data seeded with frequency rules (including skips).")
