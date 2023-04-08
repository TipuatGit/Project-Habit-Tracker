from habit_class import *
import pickle


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
        print('Enter habit names or habit option number to see details.')

    elif interface == 'add new habit':
        print("type 'add' to add new habit.")
        print("You will be prompted to enter: \n'title' which is the name of your habit.")
        print("'description' where you can describe it in detail, you can also leave it empty.")
        print("'start time' is the time at which your habit completion countdown begins.")
        print("'end time' where the countdown ends.")
        print("'type' such as daily, weekly or monthly.\n")
        print('To cancel habit entry, leave all fields empty.\n')

    elif interface == 'view all habits':
        print('to go back, type "main"')
        print('view all habits help')

    elif interface == 'my progress':
        print('to go back, type "main"')
        print('my progress help')


def main():
    '''Function prints the main interface of the program.'''
    cls()
    print("HABITS TRACKER!\n")
    print('(1) Current Habits:')
    print('(2) Add New Habit\n(3) View All Habits\n(4) My Progress')
    print('\n-type \'h\' for help. \'q\' to quit.')


def current_habits():

    #define function to retrieve data
    def get_data():
        import sqlite3
        connection = sqlite3.connect('habit_db TEST.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM habits;')
        return cursor.fetchall()
        connection.close()
        
    #clear screen to show sub-menu interface
    cls()

    #output sub-menu heading
    print('CURRENT HABITS:\n')

    #define loop controlling variable
    count = 0

    #dfine varable to store habit names from get_data()
    habit_names = []

    #extract all attributes of a habit
    #useful for taking the relevant attributes out separately
    for (id,title,desc,start,end,type,date) in get_data():
        print(f'({count}) {title} | {start} | ')
        count += 1
        habit_names.append(title)
            
##    print('(1) Walking | Duration: 0h:17m | 3')
##    print('(2) Newspaper | Duration: 1h:17m | 8')
##    print('(3) Cat feed | Coming up: 7h:3m | 6')
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
        
        elif i.isalpha():
            id, title, desc, start_time, end_time, type, date = get_data()[habit_names.index(i)]
            print('Title:', title.title())
            print('Description:', desc)
            print('Start Time:', start_time)
            print('End TIme:', end_time)
            print('Habit Type:', type)
            print('Creation Time:', date)
                
        elif i.isdigit():
            #use try-except to stop program from crashing on incorrect entry
            try:
                id, title, desc, start_time, end_time, type, date = get_data()[int(i)]
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
    while True:
        
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
                while True:
                    #define confirmation check to let user
                    #recheck if information is entered correctly.
                    confirm = input('Confirm details (y/n)? ')
                        
                    if confirm == 'y':
                        Habit(title, description, start_time, end_time, type)

                        print('\nNew habit added!\nYour new habit is being tracked.')
                        print("\nto go back, type 'main'.")
                        break

                    #if user enters no then break the loop and start again
                    elif confirm == 'n':
                        input('\npress Enter to start again...')
                        add_new_habit()
                        break
                    
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
    

def view_habits():
    '''Reads habit data from database and displayes
       all habits for the user to see, with their
       respective streaks.'''

    #clear screen to show sub-menu interface
    cls()
    print('VIEW ALL HABITS:\n')


def progress():
    '''Provides user with analyses of their habits
       so they can know what they are doing right
       and where they need to focus more.'''

    #clear screen to show sub-menu interface
    cls()
    print('MY PROGRESS:\n')
    
