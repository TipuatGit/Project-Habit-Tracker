import sqlite3
import datetime

class Habit:
    def __init__(self, title, description, duration, habit_type):
        self.title = title
        self.description = description
        self.duration = duration # amount of time within which a habit task must be completed
        self.habit_type = habit_type
        self.creation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #automatically call methods as soon as class object is created.
        self.truncate_time()
        self.add_to_database()

    

    def add_to_database(self):
        self.connection = sqlite3.connect('habit_db TEST.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?)",
                            (None, self.title, self.description, self.duration,
                             self.habit_type, self.creation_time)
                            )
        self.connection.commit()
        self.connection.close()

    def show_data(self):
        self.connection = sqlite3.connect('habit_db TEST.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('SELECT * FROM habits;')
        print(self.cursor.fetchall())
        self.connection.close()
        return self.cursor.fetchall()
        
    # a simple getter function 
    def info(self):
        print('Title:', self.title)
        print('Description:', self.description)
        print('Duration:', self.duration)
        print('Habit Type:', self.habit_type)
        print('Creation Time:', self.creation_time)

    # test function to change init property values
##    def truncate_time(self):
##        if 'minute' in self.duration:
##            self.duration = self.duration.split()
##            self.duration[1] = 'm'
##            self.duration = self.duration[0]+self.duration[1]

##    def complete_task(self)


# checking to see if things work...
watering = Habit('Water Plants',None,'30 minutes', 'weekly')
w = watering


w.info()
print()
w.show_data()
