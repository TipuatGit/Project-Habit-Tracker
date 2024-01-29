import sqlite3
import datetime

class Habit:
    def __init__(self, title, description, time_start, time_end, habit_type):
        self.title = title
        self.description = description
        self.time_start = time_start # amount of time within which a habit task must be completed
        self.time_end = time_end
        self.habit_type = habit_type
        self.creation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    def add_to_database(self):
        self.connection = sqlite3.connect('habit_db.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (None, self.title, self.description, self.time_start,
                             self.time_end, self.habit_type, self.creation_time)
                            )
        self.connection.commit()
        self.connection.close()
