from controllers import habit_controller, habit_completion_controller, analytics_controller
from models.habit import Habit, Frequency
from db.database import init_db
from datetime import datetime
import time
from scripts.seed_fixtures import create_sample_habits, seed_sample_completions
from scripts.clear_db import reset

# Habit functions
""" prints all habits """
def get_all_habits_cli():
    habits = habit_controller.get_all_habits()
    for habit in habits:
        print(habit)

""" prints all habits for a certain frequency """
def get_habits_by_frequency_cli():
    freq_input = input("Frequency (daily, weekly, biweekly, monthly): ").lower()
    habits = habit_controller.get_habits_by_frequency(freq_input)
    for habit in habits:
        print(habit)

""" gets user input to create new habit """     
def create_habit_cli():
    title = input("Title: ")
    desc = input("Description: ")
    freq_input = input("Frequency (daily, weekly, biweekly, monthly): ").lower()

    try:
        frequency = Frequency(freq_input)
    except ValueError:
        print("Invalid frequency.")
        return

    habit = Habit(
        id=0,
        title=title,
        description=desc,
        frequency=frequency,
        created_at=datetime.now()
    )

    habit_controller.add_habit(habit)
    print("Habit created.")

""" Lists all open habits for today and let's the user complete a habit for today """
def mark_completed_cli():
    show_open_tasks_for_today_cli()
    time.sleep(2)
    habit_id = int(input("Habit ID to mark as complete: "))
    habit_completion_controller.complete_habit(habit_id)

""" gets ID from user to delete a habit """
def delete_habit_cli():
    habit_id = int(input("Habit ID to delete: "))
    if habit_controller.delete_habit(habit_id):
        print("Habit deleted.")
    else:
        print("Habit not found.")

""" executes script to delete all entries from the database """
def reset_db():
    reset()
    

# Analytics functions
""" shows habits that still need to be completed today """
def show_open_tasks_for_today_cli():
    open_habits = analytics_controller.get_open_tasks_for_today()
    if not open_habits:
        print("All tasks completed for today!")
    else:
        print("Tasks still open today:")
        for habit in open_habits:
            print(f"- [{habit.id}] {habit.title} ({habit.frequency.value})")


def show_current_streak_for_habit_cli():
    habit_id = int(input("Habit ID: "))
    result = analytics_controller.get_current_streak_for_habit(habit_id)
    if result:
        print(f"{result['title']} [ID {habit_id}]: current streak → {result['streak']} periods")
    else:
        print(f"Habit ID {habit_id} not found.")


def show_current_streaks_cli():
    streaks = analytics_controller.get_current_streaks()
    for habit_id, data in streaks.items():
        print(f"{data['title']} [ID {habit_id}]: current streak → {data['streak']} periods")


def show_longest_streaks_cli():
    streaks = analytics_controller.get_longest_streaks()
    for habit_id, data in streaks.items():
        print(f"{data['title']} [ID {habit_id}]: longest streak → {data['streak']} periods")


def show_longest_streak_for_habit_cli():
    habit_id = int(input("Habit ID: "))
    result = analytics_controller.get_longest_streak_for_habit(habit_id)
    if result:
        print(f"{result['title']} [ID {habit_id}]: longest streak → {result['streak']} periods")
    else:
        print(f"Habit ID {habit_id} not found.")
  

def view_completions_cli():
    habit_id = int(input("Habit ID to view completions: "))
    completions = habit_completion_controller.get_completions(habit_id)
    print(f"Completions for Habit {habit_id}:")
    for dt in completions:
        print("-", dt.strftime("%Y-%m-%d %H:%M"))

def show_broken_habits_cli():
    broken = analytics_controller.get_broken_habits()
    if not broken:
        print("No broken habits!")
    else:
        print("Broken habits (streak interrupted):")
        for habit in broken:
            print(f"- [{habit.id}] {habit.title} ({habit.frequency.value})")
            
# MENUS
def habits_menu():
    while True:
        print("Habit Management")
        print("1. List all habits")
        print("2. List habits by frequency")
        print("3. Create a new habit")
        print("4. Mark habit as completed")
        print("5. Delete a habit")
        print("6. Reset DB")
        print("X. Back to main menu")

        choice = input("\nEnter your choice: ").strip().lower()

        if choice == "1":
            get_all_habits_cli()
        elif choice == "2":
            get_habits_by_frequency_cli()
        elif choice == "3":
            create_habit_cli()
        elif choice == "4":
            mark_completed_cli()
        elif choice == "5":
            delete_habit_cli()
        elif choice == "6":
            reset_db()
        elif choice == "x":
            break
        else:
            print("Invalid choice. Try again.")
        time.sleep(2)


def streaks_menu():
    while True:
        print("\nStreaks & Progress")
        print("1. Show open tasks for today")
        print("2. Show current streaks (all habits)")
        print("3. Show current streak (specific habit)")
        print("4. Show longest streaks (all habits)")
        print("5. Show longest streak (specific habit)")
        print("6. View completions for a specific habit")
        print("7. Show broken habits")
        print("X. Back to main menu")

        choice = input("\nEnter your choice: ").strip().lower()

        if choice == "1":
            show_open_tasks_for_today_cli()
        elif choice == "2":
            show_current_streaks_cli()
        elif choice == "3":
            show_current_streak_for_habit_cli()
        elif choice == "4":
            show_longest_streaks_cli()
        elif choice == "5":
            show_longest_streak_for_habit_cli()
        elif choice == "6":
            view_completions_cli()
        elif choice == "7":
            show_broken_habits_cli()
        elif choice == "x":
            break
        else:
            print("Invalid choice. Try again.")
        time.sleep(2)


def main_menu():
    while True:
        print("\nHabit Tracker Main Menu")
        print("1. Habit Management")
        print("2. Streaks & Progress")
        print("X. Exit")

        choice = input("\nEnter your choice: ").strip().lower()

        if choice == "1":
            habits_menu()
        elif choice == "2":
            streaks_menu()
        elif choice == "x":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    init_db()
    if not habit_controller.get_all_habits():
        create_sample_habits()
        seed_sample_completions()
    main_menu()
