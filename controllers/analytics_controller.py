from services import analytics_service
from controllers import habit_controller

def get_longest_streaks():
    """ 
        Desc: Controller to read longest streaks
        Args: /
        Returns: List of objects of habit_id and streak
    """
    streaks = analytics_service.get_longest_streak_all_habits()
    habits = {habit.id: habit.title for habit in habit_controller.get_all_habits()}
    return {habit_id: {"title": habits.get(habit_id, "Unknown"), "streak": streak} for habit_id, streak in streaks.items()}

def get_longest_streak_for_habit(habit_id: int):
    """ 
        Desc: Controller to read the longest streak for a specific habit
        Args: ID of habit 
        Returns: Object of habit title and streak
    """
    streak = analytics_service.get_longest_streak_for_habit(habit_id)
    habit = habit_controller.get_habit(habit_id)
    if habit:
        return {"title": habit.title, "streak": streak}
    return None

def get_current_streaks():
    """ 
        Desc: Controller to read current streaks 
        Args: /
        Returns: List of habits with their streaks
    """
    streaks = analytics_service.get_current_streak_all_habits()
    habits = {habit.id: habit.title for habit in habit_controller.get_all_habits()}
    return {habit_id: {"title": habits.get(habit_id, "Unknown"), "streak": streak} for habit_id, streak in streaks.items()}

def get_current_streak_for_habit(habit_id: int):
    """" 
        Desc: Controller to read the current streak for a specific habit
        Args: ID of habit 
        Returns: Object of habit name and streaks
    """
    streak = analytics_service.get_current_streak_for_habit(habit_id)
    habit = habit_controller.get_habit(habit_id)
    if habit:
        return {"title": habit.title, "streak": streak}
    return None

def get_open_tasks_for_today():
    """ 
        Desc: Controller to read open tasks for today 
        Args: /
        Returns: List of habit objects which still have not been completed today
    """
    return analytics_service.get_open_tasks_for_today()

def get_broken_habits():
    """ 
        Desc: Controller to read habit streaks that are currently broken/interrupted 
        Args: /
        Returns: List of habit objects which are currently not on a streak
    """
    return analytics_service.get_broken_habits()
