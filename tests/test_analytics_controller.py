from datetime import datetime, timedelta
from models.habit import Habit, Frequency
from db.habit_repository import insert_habit, delete_habit, get_all_habits
from db.habit_completion_repository import complete_habit
from controllers import analytics_controller


def create_test_habit(name: str):
    """Insert a test habit and return its ID"""
    habit = Habit(0, name, "", Frequency.DAILY, datetime.now())
    insert_habit(habit)
    hid = get_all_habits()[-1].id
    return hid


def test_get_longest_streaks():
    """Should return a dict with habit ID, title and streak"""
    result = analytics_controller.get_longest_streaks()
    assert isinstance(result, dict)
    for habit_id, data in result.items():
        assert "title" in data
        assert "streak" in data


def test_get_longest_streak_for_habit():
    """Create habit, mark completions, check longest streak for that habit"""
    hid = create_test_habit("C_Longest")
    now = datetime.now()
    complete_habit(hid, now - timedelta(days=2))
    complete_habit(hid, now - timedelta(days=1))
    complete_habit(hid, now)

    streak_data = analytics_controller.get_longest_streak_for_habit(hid)
    assert streak_data is not None
    assert streak_data["streak"] >= 3
    assert streak_data["title"] == "C_Longest"

    delete_habit(hid)


def test_get_current_streaks():
    """Should return a dict with habit ID, title and current streak"""
    result = analytics_controller.get_current_streaks()
    assert isinstance(result, dict)
    for habit_id, data in result.items():
        assert "title" in data
        assert "streak" in data


def test_get_current_streak_for_habit():
    """Create habit, mark completions, check current streak for that habit"""
    hid = create_test_habit("C_Current")
    now = datetime.now()
    complete_habit(hid, now - timedelta(days=1))
    complete_habit(hid, now)

    streak_data = analytics_controller.get_current_streak_for_habit(hid)
    assert streak_data is not None
    assert streak_data["streak"] >= 2
    assert streak_data["title"] == "C_Current"

    delete_habit(hid)


def test_get_open_tasks_for_today():
    """Should return list of Habit objects (may be empty)"""
    open_tasks = analytics_controller.get_open_tasks_for_today()
    assert isinstance(open_tasks, list)


def test_get_broken_habits():
    """Should return list of Habit objects (may be empty)"""
    broken = analytics_controller.get_broken_habits()
    assert isinstance(broken, list)
