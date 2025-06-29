# Habit Tracker – Python CLI Application

This is a command-line habit tracking application written in Python 3. It allows users to:

- Interact with the app via a simple CLI
- Easily test the application with five pre-defined habits
- Define and manage daily/weekly/biweekly/monthly habits
- Mark habits as completed
- Track completion history
- Analyze longest/current streaks
- Persist data using SQLite
- Automatically setup the SQLite database
- Clear the database
- Test the application with `pytest`

---

## Getting Started

### Pre-Requisites
- Have Python installed. 
    - Install Python, by downloading it from the official site: https://www.python.org/downloads/windows/
    - During the installation:
        - Check “Add Python to PATH”
        - Use the default install settings
    - To verify:
    ```bash
    python --version
    ```
- For a Mac or Linux installation check the official python website


### 1. Clone the Repository
```bash
git clone https://github.com/tjraczek/habit-tracker.git
cd habit-tracker
```

### 2. Setup a virtual environment
For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
For macOS and Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Start the program
- Run the following command to start the application
```bash
    python main.py
```

## Usage
- Easily navigate through the app by inserting the corresponding number and pressing 'Enter' at the "Enter your choice: " input (intuitive navigation)
- Exit menus or the application by inserting an 'x' or 'X' and pressing 'Enter'
- In the 'Main Menu' you get navigate to the 'Habit Management' and th 'Streak & Progress Management'.
- In the 'Habit Management' you can: 
    - list all habits 
    - list habits by frequency 
    - create a new habit 
    - mark a habit as completed (check it off for today) 
    - delete a habit 
    - reset the database

- In the 'Streaks & Progress Management' you can: 
    - show your open tasks for today
    - show the current streak for all habits and one specific habit 
    - show the longest streak (in whole usage history) for all habits or one specific habit 
    - view all dates of completions for one specific habit
    - show broken habits (habits that currently don't have a streak anymore)

## Extra functionalities of the application
- On starting the app, if there is no data, a script is executed which generates five habits 
    - The script is only executed if there are no entries at all in the database. If you want to have your custom entries only, reset the database by entering '6' in the 'Habit Management' and insert your own habits.

### Extra: Testing the app
- If you haven't install pytest yet, run the following command
```bash
    pip install pytest
```

- To run all the test execute 
```bash
    pytest
 ```
 
- To run one specific test include the path after the pytest command, e.g.
```bash
    pytest tests/test_habit_controller.py
```
### Extra: Getting help for modules
- Exit the application and enter the python environment by executing the command
```bash
    python
```
- In the python terminal, import the module you want to get help for, e.g.
```bash 
    from controllers import analytics_controller
```
- List all files in the module. There you will also find the methods.
```bash
    print(dir(analytics_controller))
```
- Get help for a specific method
```bash
    help(analytics_controller.get_broken_habits)
```
- Exit the python env with the command:
```bash
    exit() 
```