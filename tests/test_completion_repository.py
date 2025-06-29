from datetime import datetime
from db.habit_repository import insert_habit, delete_habit, get_all_habits
from db.habit_completion_repository import complete_habit, get_completions
from models.habit import Habit, Frequency

def test_complete_habit():
    # Create habit
    habit = Habit(0, "TEST_complete", "", Frequency.DAILY, datetime.now())
    insert_habit(habit)
    habit_id = get_all_habits()[-1].id

    # Complete it
    complete_habit(habit_id)

    # Check completions exist
    completions = get_completions(habit_id)
    assert completions

    # Clean up
    delete_habit(habit_id)


def test_get_completions():
    # Create habit
    habit = Habit(0, "TEST_get_completions", "", Frequency.DAILY, datetime.now())
    insert_habit(habit)
    habit_id = get_all_habits()[-1].id

    # Add completions
    complete_habit(habit_id)
    complete_habit(habit_id)

    # Check if completions have 2 entries
    completions = get_completions(habit_id)
    assert len(completions) >= 2

    # Clean up
    delete_habit(habit_id)
