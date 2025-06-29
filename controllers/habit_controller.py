from db import habit_repository
from models.habit import Frequency, Habit

def add_habit(habit: Habit):
    """" 
        Controller which adds a habit to the database
        Args: habit object
        Returns: call to habit repository
    """
    return habit_repository.insert_habit(habit)

def get_habit(id: int):
    """ 
        Desc: Controller which reads one habit
        Args: ID of habit 
        Returns: habit object
    """
    return habit_repository.get_habit_by_id(id)

def get_all_habits():
    """ 
        Desc: Controller which reads all habits
        Args: /
        Returns: List of habit objects
    """
    return habit_repository.get_all_habits()

def get_habits_by_frequency(freq_string: str):
    """ 
        Controller which gets all habits for a specific frequency
        Args: Frequency enum (daily, weekly, biweekly, monthly)
        Returns: Filtered list of habit objects
    """
    try:
        freq = Frequency(freq_string.lower())
    except ValueError:
        return None
    return habit_repository.get_habits_by_frequency(freq)

def update_habit(id: int, updated_habit: Habit):
    """ 
        Controller which updates the habit
        Args: ID of habit to be updated, Updated habit object
        Returns: Call to habit repository
    """
    return habit_repository.update_habit(id, updated_habit)

def delete_habit(id: int):
    """" 
        Controller which deletes a specific habit
        Args: ID of the habit to be deleted
        Returns: Call to habit repository
    """
    return habit_repository.delete_habit(id)
