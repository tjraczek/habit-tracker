from datetime import datetime, timedelta
from models.habit import Habit, Frequency
from db.habit_repository import insert_habit, delete_habit, get_all_habits
from db.habit_completion_repository import complete_habit
from services import analytics_service


def create_test_habit(name: str, frequency=Frequency.DAILY):
    """Insert a test habit and return its real ID"""
    habit = Habit(
        id=0,
        title=name,
        description="Test habit",
        frequency=frequency,
        created_at=datetime.now()
    )
    insert_habit(habit)
    habit_id = get_all_habits()[-1].id
    return habit_id


def test_get_periods():
    """Test splitting completions into periods for daily habits"""
    start = datetime(2024, 1, 1)
    completions = [start + timedelta(days=i) for i in range(3)]
    periods = analytics_service.get_periods(completions, Frequency.DAILY)
    assert len(periods) == 3


def test_are_consecutive():
    """Test consecutive daily periods"""
    day1 = datetime(2024, 1, 1).date()
    day2 = datetime(2024, 1, 2).date()
    day4 = datetime(2024, 1, 4).date()
    assert analytics_service.are_consecutive(day1, day2, Frequency.DAILY)
    assert not analytics_service.are_consecutive(day1, day4, Frequency.DAILY)


def test_calculate_longest_streak():
    """Test longest streak calculation with a gap"""
    start = datetime(2024, 1, 1)
    completions = [
        start,
        start + timedelta(days=1),
        start + timedelta(days=2),
        start + timedelta(days=4)
    ]
    longest = analytics_service.calculate_longest_streak(completions, Frequency.DAILY)
    assert longest == 3


def test_calculate_current_streak():
    """Test current streak calculation with a broken period"""
    start = datetime(2024, 1, 1)
    completions = [
        start,
        start + timedelta(days=1),
        start + timedelta(days=2),
        start + timedelta(days=4),
        start + timedelta(days=5)
    ]
    current = analytics_service.calculate_current_streak(completions, Frequency.DAILY)
    assert current == 2


def test_longest_streak_for_habit():
    """Insert a habit, add completions, check longest streak"""
    habit_id = create_test_habit("TEST_longest_streak")
    now = datetime.now()

    # Simulate 3 daily completions in a row
    complete_habit(habit_id, now - timedelta(days=2))
    complete_habit(habit_id, now - timedelta(days=1))
    complete_habit(habit_id, now)

    streak = analytics_service.get_longest_streak_for_habit(habit_id)
    assert streak >= 3

    delete_habit(habit_id)


def test_current_streak_for_habit():
    """Insert a habit, add completions, check current streak"""
    habit_id = create_test_habit("TEST_current_streak")
    now = datetime.now()

    # Mock 2 daily completions in a row
    complete_habit(habit_id, now - timedelta(days=1))
    complete_habit(habit_id, now)

    streak = analytics_service.get_current_streak_for_habit(habit_id)
    assert streak >= 2

    delete_habit(habit_id)


def test_longest_streak_all_habits():
    """Check that longest streaks for all habits return a valid dict."""
    result = analytics_service.get_longest_streak_all_habits()

    # Should be a dict with entries
    assert isinstance(result, dict)
    for habit_id, streak in result.items():
        assert streak >= 0 


def test_current_streak_all_habits():
    """Check that current streaks for all habits return a valid dict with integer values."""
    result = analytics_service.get_current_streak_all_habits()

    # Should be a dict
    assert isinstance(result, dict)

    # Keys should be habit IDs (ints) and values should be ints
    for habit_id, streak in result.items():
        assert isinstance(habit_id, int)
        assert isinstance(streak, int)
        assert streak >= 0


def test_get_broken_habits():
    """Check that broken habits returns a list and its items are Habit objects."""
    broken = analytics_service.get_broken_habits()

    # Should be a list
    assert isinstance(broken, list)

    # If there are broken habits, they should be Habit objects
    for habit in broken:
        assert hasattr(habit, "id")
        assert hasattr(habit, "title")
        assert hasattr(habit, "frequency")


def test_get_open_tasks_for_today():
    """Check that open tasks for today returns a list of Habit objects."""
    open_habits = analytics_service.get_open_tasks_for_today()

    # Should be a list
    assert isinstance(open_habits, list)

    # If any open tasks, they should have expected properties
    for habit in open_habits:
        assert hasattr(habit, "id")
        assert hasattr(habit, "title")
        assert hasattr(habit, "frequency")

