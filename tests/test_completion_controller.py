from datetime import datetime
from models.habit import Habit, Frequency
from db.habit_repository import insert_habit, delete_habit, get_all_habits
from controllers import habit_completion_controller


def create_test_habit(name="C_Test"):
    """Helper to add a habit and get its ID"""
    h = Habit(0, name, "", Frequency.DAILY, datetime.now())
    insert_habit(h)
    hid = get_all_habits()[-1].id
    return hid


def test_complete_habit():
    """Should mark a habit complete via controller"""
    hid = create_test_habit("C_Complete")
    habit_completion_controller.complete_habit(hid)
    completions = habit_completion_controller.get_completions(hid)
    assert completions  # should have at least 1 completion
    delete_habit(hid)


def test_get_completions():
    """Should get completions list for habit"""
    hid = create_test_habit("C_Get")
    habit_completion_controller.complete_habit(hid)
    habit_completion_controller.complete_habit(hid)
    completions = habit_completion_controller.get_completions(hid)
    assert len(completions) >= 2
    delete_habit(hid)
