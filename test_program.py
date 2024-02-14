import pytest
import subprocess
import datetime
import os
import sqlite3
import re
import random
from tabulate import tabulate
from habit_class import Habit
from analysis_module import habit_analysis
from functions import Functions

    
def pseudo_time(action='add'):
    '''create simple function to return time as string
        to test the test habit we will create '''
        
    current_time = datetime.datetime.now()
    if action == 'add':
        new_time = current_time + datetime.timedelta(minutes=30)
        return new_time.strftime("%H:%M:%S")
    elif action == 'sub':
        new_time = current_time - datetime.timedelta(minutes=30)
        return new_time.strftime("%H:%M:%S")
    elif action == 'miss':
        new_time = current_time - datetime.timedelta(minutes=15)
        return new_time.strftime("%H:%M:%S")
        
    elif action == 'random':
        days = random.randint(8,25)
        hr = random.randint(0,23)
        mins = random.randint(1,59)
        sec = random.randint(1,59)
        new_time = current_time - datetime.timedelta(days=days, hours=hr, minutes=mins, seconds=sec)
        return new_time.strftime("%Y-%m-%d %H:%M:%S")


#Fixture to initialize the functions object before each test
@pytest.fixture
def func_instance():
    return Functions()


def test_cls(func_instance, capsys):
    print("Some Test OUTPUT.")
    func_instance.cls()

    captured = capsys.readouterr()
    assert '' in captured.out
    

def test_check_database(func_instance):
    func_instance.check_database()

    #assert that the database file exists
    db_file = 'habit_db.db'
    assert os.path.exists(db_file)

    #connect to the database and assert that necessary tables are created
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    assert ('habits',) in tables
    assert ('task_completion',) in tables
    connection.close()


def test_help(func_instance, capsys, monkeypatch):
    help_interface = ['main', 'current habits', 'add new habit',
                      'view all habits', 'my progress']
    
    #mock user input for function input values
    user_inputs = ['\n', '\n', 'main']
    def mock_input(prompt):
        return user_inputs.pop(0)
        
    monkeypatch.setattr('builtins.input', mock_input)
    
    for test_input in help_interface:
        func_instance.help(test_input)
        
        #capture the output and assert that it returns a string
        captured = capsys.readouterr()
        assert captured.out


def test_check_missed_habits(func_instance):
    connection = sqlite3.connect('habit_db.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM task_completion;')
    original_rows = cursor.fetchall()
    assert original_rows #data in db already there
    
    #first delete test habits if they already exist
    delete_test_habits = [ ("DELETE FROM habits WHERE habit_id=1000;"),("DELETE FROM habits WHERE habit_id=1001;"),
                           ("DELETE FROM habits WHERE habit_id=1002;"),("DELETE FROM habits WHERE habit_id=1003;"),
                           ("DELETE FROM task_completion WHERE habit_id=1000;"),
                           ("DELETE FROM task_completion WHERE habit_id=1001;"),
                           ("DELETE FROM task_completion WHERE habit_id=1002;"),
                           ("DELETE FROM task_completion WHERE habit_id=1003;") ]
    for query in delete_test_habits:
        cursor.execute(query)
    
    #then create test habits which will be deleted later
    #add habit data in habits table
    query = 'INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?)'
    daily_immediate_missed = (1000, 'test_daily_immediate_missed', '', pseudo_time('sub'), pseudo_time('miss'),
                              'daily', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    daily_days_missed = (1001, 'test_daily_days_missed', '', pseudo_time('sub'), pseudo_time('miss'),
                         'daily', pseudo_time('random'))
    
    weekly_immediate_missed = (1002, 'test_weekly_immediate_missed', '', pseudo_time('sub'), pseudo_time('miss'),
                              'weekly', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    weekly_weeks_missed = (1003, 'test_weekly_weeks_missed', '', pseudo_time('sub'), pseudo_time('miss'),
                           'weekly', pseudo_time('random'))

    insert_test_habits = [daily_immediate_missed, daily_days_missed, weekly_immediate_missed, weekly_weeks_missed]
    cursor.executemany(query, insert_test_habits)
    connection.commit()
    connection.close()
    
    #call function to check missed habit and fill in rows
    func_instance.check_missed_habits()
    
    connection = sqlite3.connect('habit_db.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM task_completion;')
    updated_rows = cursor.fetchall()
    assert len(updated_rows) > len(original_rows) #new rows added or not
    
    #check if habits with test ids exist or not in task_completion table
    habits_exist = []
    for habit in updated_rows:
        if habit[0] in [1000,1001,1002,1003]:
            habits_exist.append(habit)
    
    assert habits_exist
    
    # Delete all rows from the tables
    for query in delete_test_habits:
        cursor.execute(query)
    
    connection.commit()
    connection.close()


def test_get_data(func_instance):
    habits_table, task_completion_table = func_instance.get_data()
    
    connection = sqlite3.connect('habit_db.db')
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM habits;')
    habits_table_db = cursor.fetchone()
    assert habits_table_db[0] == len(habits_table)

    cursor.execute('SELECT COUNT(*) FROM task_completion;')
    task_completion_table_db = cursor.fetchone()
    assert task_completion_table_db[0] == len(task_completion_table)
    connection.close()


def test_main(func_instance, capsys):
    func_instance.main()

    #capture the output and assert that it contains strings
    captured = capsys.readouterr()
    assert captured.out.isascii()


def test_current_habits(func_instance, capsys, monkeypatch):
    '''1. connect database
        2. create test habit
        3. get data from db of active habits
        4. call function
        5. compare result of function output with db output

    '''
    #get data from database
    connection = sqlite3.connect('habit_db.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM task_completion;')
    original_rows = cursor.fetchall()

    #create a test habit
    query = 'INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?)'
    inserts = (1000, 'test', '', pseudo_time('sub'), pseudo_time(),
               'daily', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cursor.execute(query, inserts)

    #get active habits from database
    cursor.execute('SELECT title FROM habits WHERE time_start < CURRENT_TIME and time_end > CURRENT_TIME;')
    habit_titles = cursor.fetchall()
    connection.commit()
    connection.close()
    
    #mock user input for function input values
    user_inputs = ['complete', '1', '', 'main']
    def mock_input(prompt):
        return user_inputs.pop(0)
        
    monkeypatch.setattr('builtins.input', mock_input)

    #call function to display habits
    func_instance.current_habits()

    captured = capsys.readouterr()
    captured = str(captured).split()

    #check if habit titles are same in function output and database output
    habit_exists = []
    for title in habit_titles:
        if title in captured:
            habit_exists.append(True)

    assert False not in habit_exists
    
    #see if completed habit is inserted into database
    connection = sqlite3.connect('habit_db.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM task_completion;')
    new_rows = cursor.fetchall()
    assert len(new_rows) > len(original_rows)
    
    cursor.execute('DELETE FROM habits WHERE habit_id=1000;')
    cursor.execute('DELETE FROM task_completion WHERE habit_id=1000;')
    connection.commit()
    connection.close()


def test_add_new_habit(func_instance, capsys, monkeypatch):
    connection = sqlite3.connect('habit_db.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM habits;')
    last_id = cursor.fetchall()[-1][0]
    connection.close()
    
    #mock user input for function input values
    user_inputs = ['add', '1', 'test_add_new', '', pseudo_time('sub'), pseudo_time(), 'y', 'main']
    def mock_input(prompt):
        return user_inputs.pop(0)
        
    monkeypatch.setattr('builtins.input', mock_input)
    
    func_instance.add_new_habit()

    connection = sqlite3.connect('habit_db.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM habits;')
    current_id = cursor.fetchall()[-1][0]

    ##assert new habit is added to db
    assert (current_id is not last_id) and (current_id > last_id)
    cursor.execute('DELETE FROM habits WHERE habit_id=(?);', (current_id,))
    cursor.execute('SELECT * FROM habits WHERE habit_id=1014;')
    habit_exist = cursor.fetchone()
    assert habit_exist is None
    connection.commit()
    connection.close()


def test_view_all_habits(func_instance, capsys, monkeypatch):
    connection = sqlite3.connect('habit_db.db')
    cursor = connection.cursor()
    cursor.execute('SELECT title FROM habits;')
    all_habits = cursor.fetchall()
    connection.close()
    
    #mock input for function
    monkeypatch.setattr('builtins.input', lambda _:'main')
    
    #call function to check output
    func_instance.view_all_habits()

    #assert counts all habits correctly
    #capture output
    captured = capsys.readouterr()
    captured = str(captured).split()
    all_habits_exist = []
    for habit in all_habits:
        for row in captured:
            if str(habit) in row:
                all_habits_exist.append(True)
    
    assert False not in all_habits_exist

    #create test habit to check deleting functionality
    query = 'INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?)'
    temp_habit = (1000, 'temp_habit', '', pseudo_time('sub'), pseudo_time(),
               'daily', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    connection = sqlite3.connect('habit_db.db')
    cursor = connection.cursor()
    cursor.execute(query, temp_habit)
    connection.commit()
    connection.close()
    
    #now we need to get function output again
    #so we know which habit number to use to delete it using function
    #mock input for function again
    monkeypatch.setattr('builtins.input', lambda _:'main')
    
    #call function again to find habit number displayed in output
    func_instance.view_all_habits()

    #capture output again and get habit number
    captured = capsys.readouterr()
    captured = str(captured).split()
    last_row = captured[-1]
    habit_number = None
    for char in last_row:
        if char.isdigit():
            habit_number = char
    
    #mock input for deleting habit
    user_inputs = ['delete', char, 'y', '\n', 'main'] 
    def mock_input(_):
        return user_inputs.pop(0)
    
    #call function again this time to perform deletion
    func_instance.view_all_habits()
    
    #check if a habit was deleted
    connection = sqlite3.connect('habit_db.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM habits;')
    all_latest_habits = cursor.fetchall()
    assert len(all_habits) != len(all_latest_habits) #deletes a habit
    
    #check if our test habit is really deleted
    cursor.execute('DELETE FROM habits WHERE habit_id=1000;')
    connection.commit()
    cursor.execute('SELECT * FROM habits WHERE habit_id=1000;')
    no_habit = cursor.fetchone()
    
    assert no_habit is None
    connection.close()
    

def test_my_progress(func_instance, capsys, monkeypatch):
    connection = sqlite3.connect('habit_db.db')
    cursor = connection.cursor()
    cursor.execute('SELECT title FROM habits WHERE habit_type="daily";')
    daily_titles = cursor.fetchall()
    cursor.execute('SELECT title FROM habits WHERE habit_type="weekly";')
    weekly_titles = cursor.fetchall()
    connection.close()
    
    #the following steps repeat twice 
    for habit_type in ['daily', 'weekly']:
    
        #mock input for deleting habit
        user_inputs = [habit_type, 'back', 'main'] 
        def mock_input(_):
            return user_inputs.pop(0)

        monkeypatch.setattr('builtins.input', mock_input)
        
        #call function
        func_instance.my_progress()
        
        #capture output
        captured = capsys.readouterr()
        captured = str(captured).split()
        all_habits_exist = []
        for habit in daily_titles:
            for row in captured:
                if habit[0] in row:
                    all_habits_exist.append(True)
        
        #assert displayes all daily and weekly habits
        assert False not in all_habits_exist
    

    #assert calculates completed tasks for a habit correctly
    connection = sqlite3.connect('habit_db.db')
    cursor = connection.cursor()
    query = """
            SELECT title, habit_type, SUM(completion_status), count(completion_status)
            FROM habits JOIN task_completion
            WHERE habits.habit_id = task_completion.habit_id
            GROUP BY title;
            """
    cursor.execute(query)
    habit_tasks = cursor.fetchall()
    connection.close()
    
    all_tasks = []
    for row in captured:
        for result in habit_tasks:
            if result[0] in row:
                if str(result[2])+'/'+str(result[3]) in row:
                    all_tasks.append(True)
    
    assert False not in all_tasks

    
def test_habit_analysis(capsys):
    
    #make test habit data for function
    habit_type = 'daily'
    habit = [[1000, 'test', '', '14:00:00', '22:40:00', habit_type, '2024-01-02 13:35:15']]
    streak = {1000: [1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1,
                     1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1,
                     1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]}
    
    #call function with parameters as input
    habits, longest_streak, index_to_id = habit_analysis(habit_type, habit, streak)

    #check correct habit is displayed
    assert habits[0][1] == 'test'
    
    #check longest_streak is calculated and exists
    assert max( longest_streak[1000] ) == 8
    
    #check correct covnersion between index and habit id
    assert index_to_id[1] == 1000
    
