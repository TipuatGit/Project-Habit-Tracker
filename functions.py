from habit_class import *
import sqlite3
from tabulate import tabulate

def cls():
    '''function that clears the terminal screen.'''
    import subprocess,os
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)


#program closing function, can be needed to save files and then close program
##def close():
##    '''Terminates the program.'''
##    pass

def help(interface = 'main'):
    
    if interface == 'main':
        print('\nWelcome to HABITS TRACKER!\n')
        print('How to navigate around the program?\nYou can enter the names of options, with or without caps.')
        print('OR you can enter numbers of the given options.\n')
        print('This applies anywhere in the program where you can see options with numbers!\n')
        print("You can also type 'h' for help anywhere in the program.\nExcept when entering some data.")
        print("\nTo get back to main menu, type 'main' in any sub-menu.")
        input('\npress Enter to close help...')
        main()

    elif interface == 'current habits':
        print('Enter habit number to see details.')

    elif interface == 'add new habit':
        print("type 'add' to add new habit. You will be prompted to enter:")
        print('- "type" such as daily, weekly or monthly.\n')
        print('\n- "title" which is the name of your habit.')
        print('- "description" where you can describe it in detail, you can also leave it empty.')
        print('- "start time" is the time at which your habit completion countdown begins.')
        print('- "end time" where the countdown ends.')
        print('To cancel habit entry, leave all fields empty.\n')
        print('\nto go back, type "main"')

    elif interface == 'view all habits':
        print('to view details of any habit, enter the habit number listed.')
        print("type 'delete' to delete a habit. this will remove all habit data and performance metrics!")        
        print('\nto go back, type "main"')

    elif interface == 'my progress':
        print('my progress help')
        print('\nto go back, type "main"')


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
    print('(1) Current Habits:')
    print('(2) Add New Habit\n(3) View All Habits\n(4) My Progress')
    print('\n-type \'h\' for help. \'q\' to quit.')


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

    #define list to store habit names for later use
    habit_names = []
    #extract all attributes of a habit
    #useful for taking the relevant attributes out separately
    for (id,title,desc,start,end,type,date) in habits_table:
        count += 1
        habit_names.append(title)
        display_habits.append([count,title, start])
    #display the habits
    headers = ["", "Title", "Duration", "Streak"] # streak data not shown as of yet
    print(tabulate(display_habits, headers=headers, tablefmt='orgtbl'))
          
##    print('(1) Walking | Duration: 0h:17m | 3')

    print('\ntype "main" to go back.')

    #define input variable
    i=''
    #start loop, check if input is digit. if yes, use it to
    #retrieve data of habit at the digit position, If digit
    #out of range, let user know. IF input is character, let
    #user get help, quit program or goto menu.
    while True:
        i = input('>> ')
        if i == 'h':
            help('current habits')
        elif i == 'q':
            quit()
        elif i == 'main':
            main()
            break
                
        elif i.isdigit() and (int(i)>0) and (int(i)<= len(habits_table)):
            #use try-except to stop program from crashing on incorrect entry
            try:
                id, title, desc, start_time, end_time, type, date = habits_table[int(i)-1]
                print('Title:', title)
                print('Description:', desc)
                print('Start Time:', start_time)
                print('End TIme:', end_time)
                print('Habit Type:', type)
                print('Creation Time:', date)
                 
            except IndexError:
                print('incorrect entry!')
                

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
    loop = True
    while loop:
        
        i = input('>> ')                
        if i == 'add':
                
            type = input('>> Type: ')
            title = input('>> Title: ').lower()
            description = input('>> Description: ')
            start_time = input('>> Start Time: ')
            end_time = input('>> End Time: ')

            #define a way to cancel new habit entry.
            #due to simplicity of CLI, leaving empty fields should indicate
            #to the program that habit entry is cancelled.
            if type + title + description + start_time + end_time == '':
                print('\nProcess cancelled. No habit added.')
                print("\nto go back, type 'main'.")
                break
            else:
                
                #define a check for if user enters values other than expected
                inner_loop = True
                while inner_loop:
                    #define confirmation check to let user
                    #recheck if information is entered correctly.
                    confirm = input('Confirm details (y/n)? ')
                        
                    if confirm == 'y':
                        Habit(title, description, start_time, end_time, type)

                        print('\nNew habit added!\nYour new habit is being tracked.')
                        print("\nto go back, type 'main'.")
                        inner_loop = False
                        loop = False

                    #if user enters no then break the loop and start again
                    elif confirm == 'n':
                        input('\npress Enter to start again...')
                        add_new_habit()
                        inner_loop = False
                    
                    elif confirm != 'y' or confirm != 'n':
                        print('\nEnter valid information.\n')
                #break
                    
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

    #define loop controlling variable
    count = 0

    confirm = ''

    #define list to store habits from habits_table
    display_habits = []

    #define list to store habit names for later use
    habit_names = []
    #extract all attributes of a habit
    #useful for taking the relevant attributes out separately
    for (id,title,desc,start,end,type,date) in habits_table:
        count += 1
        habit_names.append(title)
        display_habits.append([count,title, start])
    #display habits
    headers = ["", "Title", "Duration", "Streak"]
    print(tabulate(display_habits, headers=headers, tablefmt='orgtbl'))

    print('\n-type \'h\' for help.')

    #define input variable
    i=''
    #start loop, check if input is digit. if yes, use it to
    #retrieve data of habit at the digit position, If digit
    #out of range, let user know. IF input is character, let
    #user get help, quit program or goto menu.
    loop = True
    while loop:
        i = input('>> ')
        if i == 'h':
            help('view all habits')
        elif i == 'q':
            quit()
        elif i == 'main':
            main()
            break
        elif i == 'delete':
            cls()
            print('VIEW ALL HABITS:\n')
            count = 0
            display_habits = []
            for (id,title,desc,start,end,type,date) in habits_table:
                display_habits.append([id,title])
            
            headers = ["ID", "Title"]
            print(tabulate(display_habits, headers, tablefmt='orgtbl'))

            
            i = input('\nenter habit ID to delete a habit: ')
            confirm = input('are you sure you want to delete this habit (y/n)? ')
            while i.isdigit() and (int(i) <= len(habit_names)):
                if confirm == 'y':
                    connection = sqlite3.connect('habit_db TEST.db')
                    cursor = connection.cursor()
                    cursor.execute('DELETE FROM habits WHERE habit_id = {};'.format(i))
                    connection.commit()
                    connection.close()
                    print('Habit deleted successfully.\npress Enter to go back.')
                    view_all_habits()
                    loop = False
                    break
                elif confirm == 'n':
                    loop = False
                    view_all_habits()
                    break
                
        elif i.isdigit():
            #use try-except to stop program from crashing on incorrect entry
            try:
                id, title, desc, start_time, end_time, type, date = habits_table[int(i)]
                print('Title:', title)
                print('Description:', desc)
                print('Start Time:', start_time)
                print('End TIme:', end_time)
                print('Habit Type:', type)
                print('Creation Time:', date)
                 
            except IndexError:
                print('incorrect entry!')


def my_progress():
    '''Provides user with analyses of their habits
       so they can know what they are doing right
       and where they need to focus more.'''

    #clear screen to show sub-menu interface
    cls()
    print('MY PROGRESS:\n')
    
