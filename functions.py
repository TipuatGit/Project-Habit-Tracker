from habit_class import *
import subprocess
import os
import sqlite3
from tabulate import tabulate
import re

def cls():
    '''function that clears the terminal screen.'''
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)


def help(interface = 'main'):
    
    if interface == 'main':
        print('\nWelcome to HABITS TRACKER!\n')
        print('How to navigate around the program?\nYou enter numbers of the given options.\n')
        print('This applies anywhere in the program where you can see options with numbers!\n')
        print("You can also type 'h' for help anywhere in the program.\nExcept when entering some data.")
        print("\nTo get back to main menu, type 'main' in any sub-menu.")
        input('\npress Enter to close help...')
        main()

    elif interface == 'current habits':
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
        print('Enter "complete" to complete a habit task.')
        print("Type 'delete' to delete a habit. this will remove all habit data and performance metrics!")        
        print('\nTo go back, type "main"')

    elif interface == 'my progress':
        print('Here you can view different statistics about your habits.')
        print('Type "daily" to view daily habits.')
        print('Type "weekly" to view weekly habits.')
        print('Type "streak" to view streak of all habits.')
        print('\nTo go back, type "main"')


def check_missed_habits():
    
    current_time = datetime.datetime.now()

    habits_table, _ = get_data()

    for (id, title, desc, start, end, type, date) in habits_table:
        start_time = datetime.datetime.strptime(start, "%H:%M:%S").time()
        end_time = datetime.datetime.strptime(end, '%H:%M:%S').time()

        if type == 'daily':
            print('checking daily')
            #if there's time for daily habit then do nothing
            if (current_time.time() > start_time) and (current_time.time() < end_time):
                print('still time')
                pass
            
            #if time has passed then check if entry was made
            elif (current_time.time() > end_time):
                connection = sqlite3.connect('habit_db TEST.db')
                cursor = connection.cursor()
                query = "SELECT * FROM task_completion WHERE habit_id = ? AND DATE(completion_time) = DATE(?)"
                cursor.execute(query, (id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                existing_record = cursor.fetchone()
                print('time greater')
                #if no entry is found then habit is missed so enter 0
                if not existing_record:
                    print('no rec')
                    query = "INSERT INTO task_completion (habit_id, completion_status, completion_time) VALUES (?,?,?)"
                    cursor.execute(query, (id, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    connection.commit()
                print('end reached')

        elif type == 'weekly':
            print('checking weeky')
            #find the last entry in the database
            connection = sqlite3.connect('habit_db TEST.db')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM task_completion WHERE habit_id = ?", (id,))

            try:
                record = cursor.fetchall()[-1]

                #get days from last entry
                last_entry = datetime.datetime.strptime(record[2], "%Y-%m-%d %H:%M:%S")
                days = (current_time - last_entry).days

                #check if 7 days have passed or not
                if days > 7:
                    print('>7')
                    query = "INSERT INTO task_completion (habit_id, completion_status, completion_time) VALUES (?,?,?)"
                    cursor.execute(query, (id, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    connection.commit()
                    
                elif days == 7:
                    print('==7')
                    #if a week is over then check if time is over or not
                    if (current_time.time() > start_time) and (current_time.time() < end_time):
                        print('still time for weekly')
                    elif (current_time.time() > end_time):
                        #if time is over then enter 0 into database
                        query = "INSERT INTO task_completion (habit_id, completion_status, completion_time) VALUES (?,?,?)"
                        cursor.execute(query, (id, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        connection.commit()
                        print('0 inserted')
                elif days < 7:
                    print('<7')
                    pass
                
                connection.close()
            except IndexError:
                pass


def get_data():
    #define function to retrieve all tables from database
    connection = sqlite3.connect('habit_db TEST.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM habits;')
    habits_table = cursor.fetchall()
    cursor.execute('SELECT * FROM task_completion;')
    task_completion_table = cursor.fetchall()
    connection.close()
    return habits_table, task_completion_table
    

def main():
    '''Function prints the main interface of the program.'''
    cls()
    print("HABITS TRACKER!\n")
    print('(1) Current Habits')
    print('(2) Add New Habit\n(3) View All Habits\n(4) My Progress')
    print('\nType \'h\' for help. \'q\' to quit.')


def current_habits():
    
    #clear screen to show sub-menu interface
    cls()

    #get data from database tables
    habits_table, task_completion_table = get_data()
    
    #output sub-menu heading
    print('CURRENT HABITS:\n')
    
    #define loop controlling variable
    count = 0
    #define list to store some habit attributes from habits_table
    display_habits = []
    
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
                print('tsk id n date met') 
                task_completion_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()
                if task_completion_date == current_time.date():
                    print('record exists.')
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
    
    #display the habits
    headers = ["", "Title", "Time Left"]
    print(tabulate(display_habits, headers=headers, tablefmt='orgtbl'))

    print("\nType 'h' for help.")

    #define input variable
    i=''
    #start loop, check if input is digit. if yes, use it to
    #retrieve data of habit at the digit position, If digit
    #out of range, let user know. IF input is character, let
    #user get help, quit program or goto menu.
    while True:
        i = input('>> ')
        condition = i.isdigit() and (int(i)>0) and (int(i)<= len(habits_table))
        if i == 'h':
            help('current habits')
        elif i == 'q':
            quit()
        elif i == 'main':
            main()
            break
        elif condition == True:
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
                    connection = sqlite3.connect('habit_db TEST.db')
                    cursor = connection.cursor()
                    query = "INSERT INTO task_completion (habit_id, completion_status, completion_time) VALUES (?,?,?)"
                    cursor.execute(query, (int(habit)-1, 1, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    connection.commit()
                    connection.close()
                    input('Task completed!\n\npress Enter to continue.') # INCORRECT HABITS COMPLETED. FIX ERROR    
                    current_habits()
                    break
                else:
                    input("Incorrect entry!.\n\npress Enter to start again...")
                    current_habits()
                    break

        #user enters anything else, start again.
        elif i not in ['h', 'q', 'main', condition, 'complete']:
            current_habits()
            break


def add_new_habit():
    '''add_new_habit is a function that adds new habit
       and stores it in the database.

       It prompts the user to enter 6 inputs; type, title,
        description, start time and end time,.'''

    #clear screen to show sub-menu interface
    cls()
    
    #define a variable to control the conditional statement
    confirm = ''
    
    print('ADD NEW HABIT:\n')
    print('Type \'h\' to see help.\n')

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
                add_new_habit()
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
                add_new_habit()
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
                        Habit(title, description, start_time, end_time, type)

                        print('\nNew habit added!\nYour new habit is being tracked.')
                        print("\nTo go back, type 'main'.")
                        break

                    #if user enters no then break the loop and start again
                    elif confirm == 'n':
                        input('\npress Enter to start again...')
                        add_new_habit()
                        break
                    
                    elif confirm != 'y' or confirm != 'n':
                        print('\nEnter valid information.\n')
                    
        elif i == 'h':
            help('add new habit')
        elif i == 'q':
            quit()
        elif i == 'main':
            main()
            break

        #user enters anything else, start again.
        elif i not in ['add', 'h', 'q', 'main']:
            add_new_habit()
            break


def view_all_habits():
    '''Reads habit data from database and displayes
       all habits for the user to see, with their
       respective streaks.'''

    #clear screen to show sub-menu interface
    cls()
    print('VIEW ALL HABITS:\n')

    habits_table, task_completion_table = get_data()
    
    count = 0 #define loop controlling variable
    display_habits = [] #define list to store some habit attributes from habits_table
    index_to_id = {} #define dict to convert between habit id and display index
    
    #extract all attributes of a habit
    #useful for taking the relevant attributes out separately
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
    for row in range(len(display_habits)):
        try:
            display_habits[row].append(sum(streak[row]))
        except KeyError:
            #in case habit task has not yet started, streak wont exist.
            display_habits[row].append('-')
    
    #display the habits
    headers = ["", "Title", 'Type', "Streak"]
    print(tabulate(display_habits, headers=headers, tablefmt='orgtbl'))
    print('\nType \'h\' for help.')

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
            help('view all habits')
        elif i == 'q':
            quit()
        elif i == 'main':
            main()
            break
        elif i == 'delete':
            while True:
                i = input('\nEnter habit number to delete a habit: ')
                if not ( i.isdigit() and (int(i) <= len(display_habits)) and (int(i) >= 0) ):
                    print('Incorrect entry!')
                else:
                    break

            confirm = input('Are you sure you want to delete this habit (y/n)? ')
            if confirm == 'y':
                connection = sqlite3.connect('habit_db TEST.db')
                cursor = connection.cursor()
                cursor.execute('DELETE FROM habits WHERE habit_id=?;', (index_to_id[int(i)],))
                cursor.execute('DELETE FROM task_completion WHERE habit_id=?;', (index_to_id[int(i)],))
                connection.commit()
                connection.close()
                input('Habit deleted successfully.\npress Enter to go back.')
                view_all_habits()
                loop = False
              
            elif confirm == 'n':
                input('No habit deleted. press Enter.')
                loop = False
                view_all_habits()
                
            elif confirm != 'y' or confirm != 'n':
                print('Incorrect entry!')
                input('\npress Enter to start again...')
                view_all_habits()
                loop = False
                
        elif condition:          
            id, title, desc, start_time, end_time, type, date = habits_table[int(i)-1]
            print('Title:', title)
            print('Description:', desc)
            print('Start Time:', start_time)
            print('End Time:', end_time)
            print('Habit Type:', type)
            print('Creation Time:', date)
            previous_output = True
                 
        elif i == 'complete':
            #take habit number, insert data into database 
            habit = input('Enter habit number to complete task: ')
            if habit.isdigit() and (int(habit)>0) and (int(habit)<= len(habits_table)):
                connection = sqlite3.connect('habit_db TEST.db')
                cursor = connection.cursor()
                query = "INSERT INTO task_completion (habit_id, completion_status, completion_time) VALUES (?,?,?)"
                cursor.execute(query, (int(habit)-1, 1, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                connection.commit()
                connection.close()
                input('Task completed!\n\npress Enter to continue.')
                current_habits()
                break
        
        #user enters anything else, start again.
        elif i not in ['h', 'q', 'main', 'delete']:
            view_all_habits()
            break


def my_progress():
    '''Provides user with analyses of their habits
       so they can know what they are doing right
       and where they need to focus more.'''

    #clear screen to show sub-menu interface
    cls()
    print('MY PROGRESS:\n')
    print('Type \'h\' for help.')

    habits_table, task_completion_table = get_data()
    
    while True:
        i = input('>> ')

        if i == 'h':
            help('my progress')
        elif i == 'q':
            quit()
        elif i == 'main':
            main()
            break

        elif i == 'daily':
            for item in habits_table:
                if item[5] == 'daily':
                    print(item[1])

        elif i == 'weekly':
            for item in habits_table:
                if item[5] == 'weekly':
                    print(item[1])

        elif i == 'streak':
            #get stread data from task_completion table in database
            streak = {}
            for id, stat, time in task_completion_table:
                if id in streak.keys():
                    streak[id].append(stat)
                else:
                    streak.setdefault(id, [stat])

            #for each habit, store all streaks in list, and
            #store that list in dictionary mapped to habit id
            longest_streak = {}
            for id in range(len(streak)):
                s = streak[id]
                longest_streak.setdefault(id, [])
                longest = 0
                for task_count in s:
                    if task_count == 1:
                        longest += task_count
                    elif longest >0:
                        longest_streak[id].append(longest)
                        longest = 0
                if longest >0:
                        longest_streak[id].append(longest)
                        
                print(longest_streak)

            #prepare data to display
            display_habits = []
            for item in range(len(habits_table)):
                if list(longest_streak.keys())[item] == habits_table[item][0]:
                    display_habits.append([habits_table[item][1],max(longest_streak[item])])
            #display the habits
            headers = ["Title", "Max Streak"]
            print(tabulate(display_habits, headers=headers, tablefmt='orgtbl'))
