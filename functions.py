import subprocess
import datetime
import os
import sqlite3
import re
from tabulate import tabulate
from habit_class import Habit
from analysis_module import habit_analysis


class Functions:
    """A class containing utility functions for the habits tracker program.

    This class provides methods for clearing the terminal screen,
    checking and creating a database for habit tracking, displaying
    interface, completing and adding habit tasks, viewing all habits
    and details of habits, progress of user for individual habits
    with analysis of their progression.
    """

    
    def __init__(self):
        '''Initialize the MyClass instance.'''
        pass


    def cls(self):
        '''Method clears the terminal screen.'''
        subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)


    def check_database(self):
        '''Method checks if database exists. If it does not then creates one.'''

        #create database variable and get path of database
        db = 'habit_db.db'
        database_path = os.path.join(os.getcwd(), db)

        #create databse if it doesnt exist
        if not os.path.exists(database_path):
            connection = sqlite3.connect(database_path)
            cursor = connection.cursor()

            #create "habits" table
            cursor.execute('''CREATE TABLE habits (
                habit_id      INTEGER       PRIMARY KEY AUTOINCREMENT,
                title         VARCHAR (30)  NOT NULL,
                description   VARCHAR (100),
                time_start    TIME          NOT NULL,
                time_end      TIME          NOT NULL,
                habit_type    VARCHAR (9)   NOT NULL,
                creation_time DATETIME      NOT NULL
            )''')

            #create "task_completion" table
            cursor.execute('''CREATE TABLE task_completion (
                habit_id          INTEGER  REFERENCES habits (habit_id) ON DELETE CASCADE
                                           NOT NULL,
                completion_status BOOLEAN  NOT NULL,
                completion_time   DATETIME
            )''')
            connection.close()


    def help(self, interface = 'main'):
        '''Method provides various help features for the user at different stages in the program.'''
        
        if interface == 'main':
            print('\nWelcome to HABITS TRACKER!\n')
            print('How to navigate around the program?\nYou enter numbers of the given options.\n')
            print('This applies anywhere in the program where you can see options with numbers!\n')
            print("You can also type 'h' for help anywhere in the program.\nExcept when entering some data.")
            print("\nTo get back to main menu, type 'main' in any sub-menu.")
            input('\npress Enter to close help...')
            self.main()

        elif interface == 'current habits':
            print('Habits will be available when their time starts.')
            print('Enter habit number to see details.')
            print('Enter "complete" to complete a habit task.')
            print('\nTo go back, type "main"')

        elif interface == 'add new habit':
            print("Type 'add' to add new habit. You will be prompted to enter:")
            print('- "type" such as daily or weekly.')
            print('- "title" which is the name of your habit.')
            print('- "description" where you can describe it in detail, you can also leave it empty.')
            print('- "start time" is the time at which your habit completion countdown begins.')
            print('- "end time" where the countdown ends.')
            print('To cancel habit entry, leave all fields empty.')
            print('\nTo go back, type "main"')

        elif interface == 'view all habits':
            print('To view details of any habit, enter the habit number listed.')
            print("Type 'delete' to delete a habit. this will remove all habit data and performance metrics!")        
            print('\nTo go back, type "main"')

        elif interface == 'my progress':
            print('Here you can view different statistics about your habits.')
            print('Type "daily" to view daily habits.')
            print('Type "weekly" to view weekly habits.')
            print('Type habit number to view details. Details show \'habit name\' and \'progress\'.')
            print('Progress shows positive and negative numbers which are habit streak and missed days respectively.')
            print('Type \'back\' to go back to My Progress menu from a sub-menu')
            input('\npress Enter to close help...')
            self.my_progress()

    def check_missed_habits(self):
        '''Method checks for missed habit tasks and enters missing data into the database.'''
        
        current_time = datetime.datetime.now()
        habits_table, task_completion_table = self.get_data()
        connection = sqlite3.connect('habit_db.db')
        cursor = connection.cursor()

        for (id, title, desc, start, end, type, date) in habits_table:
            start_time = datetime.datetime.strptime(start, "%H:%M:%S").time()
            end_time = datetime.datetime.strptime(end, '%H:%M:%S').time()
            
            #if there's time for daily habit then do nothing
            if type == 'daily':
                
                #get all task completions for a habit
                this_daily_habit = [row for row in task_completion_table if row[0] == id]

                try:
                    #check how many days passed since last entry was made
                    last_entry = datetime.datetime.strptime(this_daily_habit[-1][-1], "%Y-%m-%d %H:%M:%S")
                    days = (current_time - last_entry).days
                    
                    #add missed habits if days > 1
                    if days > 1:
                        for day in range(days):
                            
                            query = "INSERT INTO task_completion (habit_id, completion_status, completion_time) VALUES (?,?,?)"
                            cursor.execute(query, (id, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                            connection.commit()
                            
                    if (current_time.time() > start_time) and (current_time.time() < end_time):
                        pass
                    
                    #if time has passed then check if entry was made
                    elif (current_time.time() > end_time):
                        query = "SELECT * FROM task_completion WHERE habit_id = ? AND DATE(completion_time) = DATE(?)"
                        cursor.execute(query, (id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        existing_record = cursor.fetchone()

                        #if no entry is found then habit is missed so enter 0
                        if not existing_record:
                            query = "INSERT INTO task_completion (habit_id, completion_status, completion_time) VALUES (?,?,?)"
                            cursor.execute(query, (id, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                            connection.commit()
                            
                except IndexError:
                    #this error means habit was created but not even the first task has been completed
                    #resulting in an empty `this_daily_habit` list
                    #in this case we check if time to complete task has passed or not
                    #and whether more than 1 days passed from the time the habit was first defined
                    #so we can enter 0 in database
                    creation_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                    num_days = (current_time - creation_date).days
                    if num_days <= 1:
                        query = "INSERT INTO task_completion (habit_id, completion_status, completion_time) VALUES (?,?,?)"
                        cursor.execute(query, (id, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        connection.commit()
                    elif num_days > 1:
                        for x in range(num_days):
                            query = "INSERT INTO task_completion (habit_id, completion_status, completion_time) VALUES (?,?,?)"
                            cursor.execute(query, (id, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                            connection.commit()

            elif type == 'weekly':
                #find the last entry in the database
                this_weekly_habit = [row for row in task_completion_table if row[0] == id]
                
                try:
                    #get days from last entry
                    last_entry = datetime.datetime.strptime(this_weekly_habit[-1][-1], "%Y-%m-%d %H:%M:%S")
                    days = (current_time - last_entry).days
                    
                    #check if 7 days have passed or not
                    if days > 7:
                        #enter 0 into database for the number of weeks calculated
                        weeks = days//7
                        for x in range(weeks):
                            query = "INSERT INTO task_completion (habit_id, completion_status, completion_time) VALUES (?,?,?)"
                            cursor.execute(query, (id, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                            connection.commit()
                            
                    elif days == 7:
                        
                        #if a week is over then check if time is over or not
                        if (current_time.time() > start_time) and (current_time.time() < end_time):
                            pass
                        
                        elif (current_time.time() > end_time):
                            #if time is over then enter 0 into database
                            query = "INSERT INTO task_completion (habit_id, completion_status, completion_time) VALUES (?,?,?)"
                            cursor.execute(query, (id, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                            connection.commit()
                            
                    elif days < 7:
                        pass
                    
                except IndexError:
                    #this error means habit was created but not even the first task has been completed
                    #resulting in an empty `this_weekly_habit` list
                    #in this case we just check if 7 days passed from the time the habit was first defined
                    #so we can enter 0 in database
                    creation_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                    num_days = (current_time - creation_date).days
                    if num_days > 7:
                        weeks = num_days // 7
                        for x in range(weeks):
                            query = "INSERT INTO task_completion (habit_id, completion_status, completion_time) VALUES (?,?,?)"
                            cursor.execute(query, (id, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                            connection.commit()
                        
        connection.close()


    def get_data(self):
        '''Method returns all habit data from the database.'''
        
        #define function to retrieve all tables from database
        connection = sqlite3.connect('habit_db.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM habits;')
        habits_table = cursor.fetchall()
        cursor.execute('SELECT * FROM task_completion;')
        task_completion_table = cursor.fetchall()
        connection.close()
        return habits_table, task_completion_table
        

    def main(self):
        '''Method prints the main interface of the program.'''
        
        self.cls()
        print("HABITS TRACKER!\n")
        print('(1) Current Habits')
        print('(2) Add New Habit\n(3) View All Habits\n(4) My Progress')
        print('\nType \'h\' for help. \'q\' to quit.')


    def current_habits(self):
        '''Method displays currently active habits on screen for user to complete.
        Habits dissappear after their set time is over.'''
        
        #clear screen to show sub-menu interface
        self.cls()

        #get data from database tables
        habits_table, task_completion_table = self.get_data()
        
        #output sub-menu heading
        print('CURRENT HABITS:\n')
        
        count = 0 #define loop controlling variable
        display_habits = [] #define list to store some habit attributes from habits_table
        index_to_id = {} #define dict to convert between habit id and display index

        
        #extract all attributes of a habit
        #allows for taking the relevant attributes out separately
        for (id,title,desc,start,end,type,date) in habits_table:
            
            #get current time and habit duration
            current_time = datetime.datetime.now()
            start_time = datetime.datetime.strptime(start, "%H:%M:%S").time()
            end_time = datetime.datetime.strptime(end, '%H:%M:%S').time()

            #check if habit has been completed before or not
            no_record_exists = True
            for task_id, task, date in task_completion_table:
                if task_id == id and date is not None:
                    task_completion_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()
                    if task_completion_date == current_time.date():
                        no_record_exists = False
                        
            #if habit completion time has started, and it has no record for the day then display the habit.
            if current_time.time() > start_time and current_time.time() < end_time and no_record_exists:
                # Calculate the duration
                duration = datetime.datetime.combine(datetime.datetime.today(), end_time) - datetime.datetime.combine(datetime.datetime.today(), current_time.time())

                # Calculate the hour and minute values
                total_minutes = int(duration.total_seconds() / 60)
                hours = total_minutes // 60
                minutes = total_minutes % 60
                duration = "{}h {}m".format(hours, minutes)
                count += 1
                display_habits.append([count,title, duration])
                #assign habit ids to index of active habits for use in completing habits
                index_to_id.setdefault(count, id)
        
        #display the habits
        headers = ["", "Title", "Time Left"]
        print(tabulate(display_habits, headers=headers, tablefmt='orgtbl'))
        
        print("\nType 'complete' to complete task\nType'h' for help.")

        #define input variable
        i=''
        #start loop, check if input is digit. if yes, use it to
        #retrieve data of habit at the digit position, If digit
        #out of range, let user know. IF input is alpha, let
        #user get help, quit program or goto menu.
        while True:
            i = input('>> ')
            condition = i.isdigit() and (int(i)>0) and (int(i)<= len(habits_table))
            if i == 'h':
                self.help('current habits')
            elif i == 'q':
                quit()
            elif i == 'main':
                self.main()
                break
            elif condition == True and len(display_habits) != 0:
                id, title, desc, start_time, end_time, type, date = habits_table[int(i)-1]
                print('Title:', title)
                print('Description:', desc)
                print('Start Time:', start_time)
                print('End Time:', end_time)
                print('Habit Type:', type)
                print('Creation Time:', date)

            elif i == 'complete':
                if len(display_habits) == 0:
                    print('No habits to complete.')

                else:
                    #take habit number, insert data into database 
                    habit = input('Enter habit number to complete task: ')
                    if habit.isdigit() and (int(habit)>0) and (int(habit)<= len(habits_table)):
                        connection = sqlite3.connect('habit_db.db')
                        cursor = connection.cursor()
                        query = "INSERT INTO task_completion (habit_id, completion_status, completion_time) VALUES (?,?,?)"
                        cursor.execute(query, (index_to_id[int(habit)], 1, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        connection.commit()
                        connection.close()
                        input('Task completed!\n\npress Enter to continue.')  
                        self.current_habits()
                        break
                    else:
                        input("Incorrect entry!\n\npress Enter to start again...")
                        self.current_habits()
                        break

            #user enters anything else, start again.
            elif i not in ['h', 'q', 'main', condition, 'complete']:
                self.current_habits()
                break


    def add_new_habit(self):
        '''Method adds new habit to the program and stores it in the database.
           It prompts the user to enter 5 inputs: type, title, description, start time and end time.'''

        #clear screen to show sub-menu interface
        self.cls()
        
        #define a variable to control the conditional statement
        confirm = ''
        
        print('ADD NEW HABIT:\n')
        print('Type \'add\' to add new habit.\nType \'h\' to see help.\n')

        #define while loop so in case user enters wrong info
        #they can fix it by repeating steps
        while True:
            
            i = input('>> ')                
            if i == 'add':
                
                type = input('please type "1" for "daily habits", "2" for "weekly habits".\n>> Type: ')

                #check if type entry is valid
                if type == '1' or type == '2':
                    pass
                else:
                    input('Enter valid information.\n\npress Enter to start again...')
                    self.add_new_habit()
                    break
                
                if type == '1':
                    type = 'daily'
                elif type == '2':
                    type = 'weekly'
                
                title = input('>> Title: ').lower()
                description = input('>> Description: ')
                print('please use the format "HH:MM:SS" for entering start and end times.')
                start_time = input('>> Start Time: ')
                end_time = input('>> End Time: ')

                #check duration entry is valid using regex.
                time_regex = re.compile(r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$')
                if not (time_regex.match(start_time) and time_regex.match(end_time)):
                    input('Enter valid information.\n\npress Enter to start again...')
                    self.add_new_habit()
                    break

                #define a way to cancel new habit entry.
                #due to simplicity of CLI, leaving empty fields should indicate
                #to the program that habit entry is cancelled.
                if type + title + description + start_time + end_time == '':
                    print('\nProcess cancelled. No habit added.')
                    print("\nTo go back, type 'main'.")

                else:
                    
                    #define a check for if user enters values other than expected
                    while True:
                        #define confirmation check to let user
                        #recheck if information is entered correctly.
                        confirm = input('Confirm details (y/n)? ')
                            
                        if confirm == 'y':
                            # instantiate object from habit_class.py
                            new_habit = Habit(title, description, start_time, end_time, type)
                            new_habit.add_to_database()
                            new_habit.make_commit()
                            new_habit.close_database()

                            print('\nNew habit added!\nYour new habit is being tracked.')
                            print("\nTo go back, type 'main'.")
                            break

                        #if user enters no then break the loop and start again
                        elif confirm == 'n':
                            input('\npress Enter to start again...')
                            self.add_new_habit()
                            break
                        
                        elif confirm != 'y' or confirm != 'n':
                            print('\nEnter valid information.\n')
                        
            elif i == 'h':
                self.help('add new habit')
            elif i == 'q':
                quit()
            elif i == 'main':
                self.main()
                break

            #user enters anything else, start again.
            elif i not in ['add', 'h', 'q', 'main']:
                self.add_new_habit()
                break


    def view_all_habits(self):
        '''Method reads habit data from database and displays all habits for the user to see,
            with their respective streaks.'''

        #clear screen to show sub-menu interface
        self.cls()
        print('VIEW ALL HABITS:\n')

        habits_table, task_completion_table = self.get_data()
        
        count = 0 #define loop controlling variable
        display_habits = [] #define list to store some habit attributes from habits_table
        index_to_id = {} #define dict to convert between habit id and display index
        
        #extract all attributes of a habit
        #useful for taking the relevant attributes out separately
        #populate display_habits and index_to_id with relevant data
        for (id,title,desc,start,end,type,date) in habits_table:
            count += 1
            index_to_id.setdefault(count, id)
            display_habits.append([count, title, type])

        #assign streak for each habit using id
        streak = {}
        for id, stat, time in task_completion_table:
            if id in streak.keys():
                streak[id].append(stat)
            else:
                streak.setdefault(id, [stat])

        #append streak data to habits data
        for row in display_habits:
            if row[0] in index_to_id.keys() and sum(streak.get(index_to_id[row[0]],[])) != 0:
                row.append(sum(streak[index_to_id[row[0]]]))
            else:
                #in case habit task has not yet started, streak wont exist.
                row.append('-')
        
        #display the habits
        headers = ["", "Title", 'Type', "Streak"]
        print(tabulate(display_habits, headers=headers, tablefmt='orgtbl'))
        print('\nType \'delete\' to delete habit.\nType \'h\' for help.')

        #define input variable
        i=''
        confirm = ''
        #start loop, check if input is digit. if yes, use it to
        #retrieve data of habit at the digit position, If digit
        #out of range, let user know. IF input is character, let
        #user get help, quit program or goto menu.

        loop = True
        while loop:
            i = input('>> ')
            condition = i.isdigit() and (int(i)>0) and (int(i)<= len(habits_table))

            if i == 'h':
                self.help('view all habits')
            elif i == 'q':
                quit()
            elif i == 'main':
                self.main()
                break
            elif i == 'delete':
                #check for correct habit number entry
                while True:
                    i = input('\nEnter habit number to delete a habit: ')
                    if not ( i.isdigit() and (int(i) <= len(display_habits)) and (int(i) >= 0) ):
                        print('Incorrect entry!')
                    else:
                        break

                confirm = input('Are you sure you want to delete this habit (y/n)? ')
                if confirm == 'y':
                    connection = sqlite3.connect('habit_db.db')
                    cursor = connection.cursor()
                    cursor.execute('DELETE FROM habits WHERE habit_id=?;', (index_to_id[int(i)],))
                    cursor.execute('DELETE FROM task_completion WHERE habit_id=?;', (index_to_id[int(i)],))
                    connection.commit()
                    connection.close()
                    input('Habit deleted successfully.\npress Enter to go back.')
                    self.view_all_habits()
                    loop = False
                  
                elif confirm == 'n':
                    input('No habit deleted. press Enter.')
                    loop = False
                    self.view_all_habits()
                    
                elif confirm != 'y' or confirm != 'n':
                    input('Incorrect entry!\npress Enter to start again...')
                    self.view_all_habits()
                    loop = False

            #display habit details on user request        
            elif condition:          
                id, title, desc, start_time, end_time, type, date = habits_table[int(i)-1]
                print('Title:', title)
                print('Description:', desc)
                print('Start Time:', start_time)
                print('End Time:', end_time)
                print('Habit Type:', type)
                print('Creation Time:', date)
            
            #user enters anything else, start again.
            elif i not in ['h', 'q', 'main', 'delete']:
                self.view_all_habits()
                break


    def my_progress(self):
        '''Method provides user with analyses of their habits so they can know what they are doing right
           and on which habits they need to focus more.'''

        #clear screen to show sub-menu interface
        self.cls()
        print('MY PROGRESS:\n')
        print('Type \'daily\' or \'weekly\' to view daily or weekly habits.\nType \'h\' for help.')

        habits_table, task_completion_table = self.get_data()

        #get streak data from task_completion table in database
        streak = {}
        for id, stat, time in task_completion_table:
            if id in streak.keys():
                streak[id].append(stat)
            else:
                streak.setdefault(id, [stat])

        main_loop = True
        while main_loop:
            i = input('>> ')

            if i == 'h':
                main_loop = False
                self.help('my progress')
            elif i == 'q':
                quit()
            elif i == 'main':
                self.main()
                break

            elif i == 'daily' or i == 'weekly':

                self.cls() #clear screen to display sub-menu

                #display menu title on screen
                if i == 'daily':
                    print('DAILY HABITS:\n')
                elif i == 'weekly':
                    print('WEEKLY HABITS:\n')

                habits, longest_streak, index_to_id = habit_analysis(i, habits_table, streak)

                #take user input for viewing habit details and other functions
                inner_loop = True
                while inner_loop:
                    i = input('\n>> ')
                    condition = i.isdigit() and (int(i)>0) and (int(i)<= len(habits))

                    if i == 'h':
                        self.help('my progress')
                    elif i == 'q':
                        quit()
                    elif condition:
                        index, title, tasks, streak = habits[int(i)-1]
                        print('Habit: ' + title)
                        print('Performance: ', longest_streak[index_to_id[int(i)]])
                    elif i == 'back':
                        inner_loop = False
                        main_loop = False
                        self.my_progress()
                    elif i not in ['h', 'q', 'back', condition]:
                        inner_loop = False
                        main_loop = False
                        self.my_progress()
                          

            #user enters anything else, start again.
            elif i not in ['h', 'q', 'main', 'daily', 'weekly']:
                self.my_progress()
                break

