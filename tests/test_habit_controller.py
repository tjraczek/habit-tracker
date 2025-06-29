from datetime import datetime
from models.habit import Habit, Frequency
from controllers import habit_controller


def test_add_and_get_habit():
    """Should add a habit and fetch it by ID"""
    habit = Habit(0, "testtest", "desc", Frequency.DAILY, datetime.now())
    habit_controller.add_habit(habit)
    habit_id = habit_controller.get_all_habits()[-1].id

    fetched = habit_controller.get_habit(habit_id)
    assert fetched is not None
    assert fetched.title == "testtest"

    habit_controller.delete_habit(habit_id)


def test_get_all_habits():
    """Should return list of habits"""
    habit = Habit(0, "testtest", "desc", Frequency.DAILY, datetime.now())
    habit_controller.add_habit(habit)
    habit_id = habit_controller.get_all_habits()[-1].id

    all_habits = habit_controller.get_all_habits()
    assert any(h.id == habit_id for h in all_habits)

    habit_controller.delete_habit(habit_id)


def test_get_habits_by_frequency():
    """Should filter by frequency"""
    habit = Habit(0, "testtest", "desc", Frequency.WEEKLY, datetime.now())
    habit_controller.add_habit(habit)
    habit_id = habit_controller.get_all_habits()[-1].id

    weekly_habits = habit_controller.get_habits_by_frequency("weekly")
    assert any(h.id == habit_id for h in weekly_habits)

    habit_controller.delete_habit(habit_id)


def test_update_habit():
    """Should update an existing habit"""
    habit = Habit(0, "testtest", "desc", Frequency.DAILY, datetime.now())
    habit_controller.add_habit(habit)
    habit_id = habit_controller.get_all_habits()[-1].id

    updated = Habit(0, "testupdated", "new desc", Frequency.WEEKLY, datetime.now())
    success = habit_controller.update_habit(habit_id, updated)
    assert success

    fetched = habit_controller.get_habit(habit_id)
    assert fetched.title == "testupdated"
    assert fetched.description == "new desc"
    assert fetched.frequency == Frequency.WEEKLY

    habit_controller.delete_habit(habit_id)


def test_delete_habit():
    """Should delete an existing habit"""
    habit = Habit(0, "H_Delete", "desc", Frequency.DAILY, datetime.now())
    habit_controller.add_habit(habit)
    habit_id = habit_controller.get_all_habits()[-1].id

    deleted = habit_controller.delete_habit(habit_id)
    assert deleted
    assert habit_controller.get_habit(habit_id) is None
