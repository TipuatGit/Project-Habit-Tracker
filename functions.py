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
        print('''\nWelcome to HABITS TRACKER!
        How to navigate around the program?
        You can enter the names of options, with or without caps.
        OR you can enter numbers of the given options.

        This applies anywhere in the program where you
        can see options with numbers!

        You can also type 'h' for help anywhere in the program.
        Except when entering some data.
        ''')

    elif interface == 'current habits':
        print('''Enter habit names or habit option number to see
              detailed habit information.''')

    elif interface == 'add new habit':
        print("You can enter 'title', 'description', 'duration' and 'type' for your new habit. type 'add' to add new habit")
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

    #extract all attributes of a habit
    #useful for taking the relevant attributes out separately
    for (id,title,desc,duration,type,date) in get_data():
        print(f'({count}) {title} | {duration} | ')
        count += 1
            
##    print('(1) Walking | Duration: 0h:17m | 3')
##    print('(2) Newspaper | Duration: 1h:17m | 8')
##    print('(3) Cat feed | Coming up: 7h:3m | 6')
    print('\nto go back, type "main"')

    i=''
    while True:
        i = input('>> ')
        if i.isdigit():
            if int(i) <= len(get_data()):
                print(get_data()[int(i)])
                
            elif int(i) >= len(get_data()):
                print('incorrect entry!')
        elif i == 'q':
            quit()
        elif i == 'h':
            help('current habits')
                

def add_new_habit():
    '''add_new_habit is a function that adds new habit
       and stores it in the database.

       It prompts the user to enter three inputs; title,
       description and duration.'''

    #clear screen to show sub-menu interface
    cls()
    
    #define a variable to control the conditional statement
    confirm = 'n'
    
    print('ADD NEW HABIT:\n')
    #define while loop so in case user enters wrong info
    #they can fix it by repeating steps
    while True:
        
        print('Type \'h\' to see help.\n')
        i = input('>> ')
        if i == 'add':
            if confirm == 'n':
                
                type = input('>> Type: ')
                title = input('>> Title: ')
                description = input('>> Description: ')
                duration = input('>> Duration: ')

                #define a way to cancel new habit entry.
                #due to simplicity of CLI, leaving empty fields
                #should indicate to the program that habit entry
                #is cancelled.
                if type + title + description + duration == '':
                    print('\nProcess cancelled. No habit added.')
                    break
                else:
                    #define confirmation check to let user
                    #recheck if information is entered correctly.
                    confirm = input('Confirm details (y/n)? ')
                
            elif confirm == 'y':
                print('\nNew habit added!\nYour new habit is being tracked.')
                break

            #define a check if user enters values other than expected
            #to prevent breaking the program (infinite loop)
            elif confirm == str():
                print('\nEnter valid information.\n')
                confirm = 'n'

        elif i == 'h':
            help('add new habit')
            
        else:
            main()
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
    
