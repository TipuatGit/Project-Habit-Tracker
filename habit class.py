import sqlite3

class Habit:
    def __init__(self, title, description, duration):
        self.title = title
        self.description = description
        self.duration = duration

    def add_to_database(self):
        self.connection = sqlite3.connect('habit_db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"INSERT INTO habits VALUES (?, ?, ?)",
                            (self.title, self.description, self.duration))
