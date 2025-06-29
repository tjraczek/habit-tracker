from datetime import datetime
from models.habit import Habit, Frequency
from db import habit_repository, database

# Helpers
def insert_test_habit(title="Test Habit", freq=Frequency.DAILY):
    habit = Habit(
        id=0,
        title=title,
        description="Test Description",
        frequency=freq,
        created_at=datetime.now()
    )
    habit_repository.insert_habit(habit)
    all_habits = habit_repository.get_all_habits()
    inserted = next((h for h in all_habits if h.title == title), None)
    assert inserted is not None
    return inserted


def delete_test_habit_by_id(habit_id):
    habit_repository.delete_habit(habit_id)


# Tests
def test_insert_and_get_habit_by_id():
    habit = insert_test_habit("Test Insert")
    fetched = habit_repository.get_habit_by_id(habit.id)

    assert fetched is not None
    assert fetched.title == "Test Insert"

    delete_test_habit_by_id(habit.id)


def test_get_habits_by_frequency():
    daily = insert_test_habit("Daily Habit", Frequency.DAILY)
    weekly = insert_test_habit("Weekly Habit", Frequency.WEEKLY)

    daily_habits = habit_repository.get_habits_by_frequency(Frequency.DAILY)
    weekly_habits = habit_repository.get_habits_by_frequency(Frequency.WEEKLY)

    assert any(h.id == daily.id for h in daily_habits)
    assert any(h.id == weekly.id for h in weekly_habits)

    delete_test_habit_by_id(daily.id)
    delete_test_habit_by_id(weekly.id)


def test_update_habit():
    habit = insert_test_habit("To Update", Frequency.MONTHLY)

    updated = Habit(
        id=habit.id,
        title="Updated Title",
        description="Updated Desc",
        frequency=Frequency.BIWEEKLY,
        created_at=datetime.now()
    )

    success = habit_repository.update_habit(habit.id, updated)
    assert success is True

    fetched = habit_repository.get_habit_by_id(habit.id)
    assert fetched.title == "Updated Title"
    assert fetched.description == "Updated Desc"
    assert fetched.frequency == Frequency.BIWEEKLY

    delete_test_habit_by_id(habit.id)


def test_delete_habit():
    habit = insert_test_habit("To Delete", Frequency.WEEKLY)
    deleted = habit_repository.delete_habit(habit.id)
    assert deleted is True

    fetched = habit_repository.get_habit_by_id(habit.id)
    assert fetched is None


def test_delete_all_habits_removes_test_habits_only():
    habit1 = insert_test_habit("Temp 1")
    habit2 = insert_test_habit("Temp 2")

    all_habits_before = habit_repository.get_all_habits()
    assert any(h.id == habit1.id for h in all_habits_before)
    assert any(h.id == habit2.id for h in all_habits_before)

    habit_repository.delete_habit(habit1.id)
    habit_repository.delete_habit(habit2.id)

    all_habits_after = habit_repository.get_all_habits()
    assert all(h.id != habit1.id and h.id != habit2.id for h in all_habits_after)
