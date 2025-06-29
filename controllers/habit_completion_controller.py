from db import habit_completion_repository

def complete_habit(habit_id: int):
    """ 
        Desc: Controller to check off a habit for today
        Args: ID of habit 
        Returns: printed string that habit has been marked as compelted
    """
    habit_completion_repository.complete_habit(habit_id)
    print(f"Habit ID {habit_id} marked as completed.")

def get_completions(habit_id: int):
    """ 
        Desc: Controller to get the dates of the completions of a specific habit
        Args: ID of habit 
        Returns: List of dates of completions for a specific habit
    """
    return habit_completion_repository.get_completions(habit_id)
