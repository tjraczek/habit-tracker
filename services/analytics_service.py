from typing import List, Dict, Union
from datetime import datetime
from models.habit import Habit, Frequency
from db.habit_repository import get_all_habits
from db.habit_completion_repository import get_completions
from typing import List, Union
from datetime import datetime
from models.habit import Frequency

# Helper method
def get_periods(completions: List[datetime], frequency: Frequency) -> List[Union[datetime.date, tuple, int]]:
    """ 
        Desc: Turns completions into periods based on habit frequency
        Args: List of completions (datetime), Frequency object
        Returns: List of periods
    """
    if not completions:
        return []

    completions.sort()

    if frequency == Frequency.DAILY:
        return [completion.date() for completion in completions]

    if frequency == Frequency.WEEKLY:
        return [completion.isocalendar()[:2] for completion in completions]

    if frequency == Frequency.BIWEEKLY:
        start_date = completions[0]
        return [((completion - start_date).days // 14) for completion in completions]

    if frequency == Frequency.MONTHLY:
        return [(completion.year, completion.month) for completion in completions]

    return []


# Helper method
def are_consecutive(previous_period, current_period, frequency: Frequency) -> bool:
    """ 
        Desc: Checks if two periods are consecutive
        Args: first period, second later period, frequency
        Returns: boolean if periods are consecutive
    """
    if frequency == Frequency.DAILY:
        # Checks if the two dates one day apart
        return (current_period - previous_period).days == 1

    if frequency == Frequency.WEEKLY:
        prev_year, prev_week = previous_period
        curr_year, curr_week = current_period

        return (
            (curr_year == prev_year and curr_week == prev_week + 1)
            or (curr_year == prev_year + 1 and prev_week == 52 and curr_week == 1)
        )

    if frequency == Frequency.BIWEEKLY:
        # checks if the dates are two periods/weeks apart
        return current_period == previous_period + 1

    if frequency == Frequency.MONTHLY:
        prev_year, prev_month = previous_period
        curr_year, curr_month = current_period

        return (
            (curr_year == prev_year and curr_month == prev_month + 1)
            or (curr_year == prev_year + 1 and prev_month == 12 and curr_month == 1)
        )

    return False

def calculate_longest_streak(completions: List[datetime], frequency: Frequency) -> int:
    """ 
        Desc: Calculates the longest streak for one single habit
        Args: list of completions, frequency
        Returns: longest streak (int)
    """
    periods = sorted(set(get_periods(completions, frequency)))
    if not periods:
        return 0

    longest = current = 1

    for i in range(1, len(periods)):
        if are_consecutive(periods[i - 1], periods[i], frequency):
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    return longest


def calculate_current_streak(completions: List[datetime], frequency: Frequency) -> int:
    """ 
        Desc: Calculates the current active streak up to today (if not broken at some point)
        Args: list of completions, frequency
        Returns: longest streak (int)
    """
    periods = sorted(set(get_periods(completions, frequency)))
    if not periods:
        return 0

    current_streak = 1

    for i in range(len(periods) - 1, 0, -1):
        if are_consecutive(periods[i - 1], periods[i], frequency):
            current_streak += 1
        else:
            break

    return current_streak


def get_longest_streak_all_habits() -> Dict[int, int]:
    """ 
        Desc: Returns the longest streak for all habits.
        Args: /
        Returns: List (Dictionary) of Habit ID (int) and streak length (int)
    """
    return {
        habit.id: calculate_longest_streak(get_completions(habit.id), habit.frequency)
        for habit in get_all_habits()
    }


def get_current_streak_all_habits() -> Dict[int, int]:
    """ 
        Desc: Returns current streak for all habits.
        Args: /
        Returns: List (Dictionary) of Habit ID (int) and streak length (int)
    """
    return {
        habit.id: calculate_current_streak(get_completions(habit.id), habit.frequency)
        for habit in get_all_habits()
    }


def get_longest_streak_for_habit(habit_id: int) -> int:
    """ 
        Desc: Returns the longest streak for one specific habit.
        Args: ID of habit (int)
        Returns: streak length of habit (int)
    """
    habit = next((h for h in get_all_habits() if h.id == habit_id), None)
    return calculate_longest_streak(get_completions(habit_id), habit.frequency) if habit else 0


def get_current_streak_for_habit(habit_id: int) -> int:
    """ 
        Desc: Returns the current streak for one specific habit
        Args: ID of habit (int)
        Returns: streak length of habit (int)
    """
    habit = next((h for h in get_all_habits() if h.id == habit_id), None)
    return calculate_current_streak(get_completions(habit_id), habit.frequency) if habit else 0


def get_broken_habits() -> List[Habit]:
    """ 
        Desc: Returns a list of habits that have been broken
        Args: /
        Returns: List of habit objects
    """
    today = datetime.now()
    brokenHabits = []

    for habit in get_all_habits():
        completions = sorted(get_completions(habit.id))
        if not completions:
            continue

        last = completions[-1]

        if habit.frequency == Frequency.DAILY:
            if (today.date() - last.date()).days > 1:
                brokenHabits.append(habit)

        elif habit.frequency == Frequency.WEEKLY:
            if (today.isocalendar()[1] - last.isocalendar()[1]) > 1 or today.isocalendar()[0] > last.isocalendar()[0]:
                brokenHabits.append(habit)

        elif habit.frequency == Frequency.BIWEEKLY:
            base = completions[0]
            current_period = (today - base).days // 14
            last_period = (last - base).days // 14
            if current_period > last_period + 1:
                brokenHabits.append(habit)

        elif habit.frequency == Frequency.MONTHLY:
            month_diff = (today.year - last.year) * 12 + today.month - last.month
            if month_diff > 1:
                brokenHabits.append(habit)

    return brokenHabits


def get_open_tasks_for_today() -> List[Habit]:
    """ 
        Desc: Returns habits that still haven't been completed today
        Args: /
        Returns: List of habit objects
    """
    today = datetime.now()
    open_habits = []

    for habit in get_all_habits():
        completions = sorted(get_completions(habit.id))
        if not completions:
            open_habits.append(habit)
            continue

        latest_completion = completions[-1]

        if habit.frequency == Frequency.DAILY:
            if latest_completion.date() != today.date():
                open_habits.append(habit)

        elif habit.frequency == Frequency.WEEKLY:
            if latest_completion.isocalendar()[:2] != today.isocalendar()[:2]:
                open_habits.append(habit)

        elif habit.frequency == Frequency.BIWEEKLY:
            base = completions[0]
            current_period = (today - base).days // 14
            latest_period = (latest_completion - base).days // 14
            if current_period != latest_period:
                open_habits.append(habit)

        elif habit.frequency == Frequency.MONTHLY:
            if (latest_completion.year, latest_completion.month) != (today.year, today.month):
                open_habits.append(habit)

    return open_habits
