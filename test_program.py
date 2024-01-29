import subprocess
import datetime
import os
import sqlite3
import re
from tabulate import tabulate
from habit_class import Habit
from analysis_module import habit_analysis
from functions import Functions
import pytest

#Fixture to initialize the functions object before each test
@pytest.fixture
def func_instance():
    return Functions()


def test_cls(func_instance, capsys):
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


def test_main(func_instance, capsys):
    func_instance.main()

    #capture the output and assert that it contains expected strings
    captured = capsys.readouterr()
    assert captured.out.isalnum()





def test_habit_analysis():
    habits, longest_streak, index_to_id = habit_analysis()

    #test that habits list contains all habits stored in database
    path = os.path.join(os.getcwd(), 'habit_db.db')
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM habits;')
    total_habits = cur.fetchone()

    assert len(habits) == total_habits
