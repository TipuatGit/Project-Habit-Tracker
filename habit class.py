import sqlite3
import datetime

class Habit:
    def __init__(self, title, description, time_start, time_end,habit_type):
        self.title = title
        self.description = description
        self.time_start = time_start # amount of time within which a habit task must be completed
        self.time_end = time_end
        self.habit_type = habit_type
        self.creation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #automatically call methods as soon as class object is created.
        #self.truncate_time()
        self.add_to_database()


    def add_to_database(self):
        self.connection = sqlite3.connect('habit_db TEST.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (None, self.title, self.description, self.time_start,
                             self.time_end, self.habit_type, self.creation_time)
                            )
        self.connection.commit()
        self.connection.close()
        

    # test function to change init property values
##    def truncate_time(self):
##        if 'minute' in self.duration:
##            self.duration = self.duration.split()
##            self.duration[1] = 'm'
##            self.duration = self.duration[0]+self.duration[1]

##    def complete_task(self)

