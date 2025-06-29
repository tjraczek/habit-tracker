from db import habit_repository

def reset():
    """ Clears all database entries. The action is irreversible. """
    print("Do you want to reset the database? (IRREVERSIBLE)")
    print("y/n")

    response = input().strip()
    if (response == "y"):
        habit_repository.delete_all_habits()
        print("All habits and completions deleted.")