def cls():
    '''function that clears the terminal screen.'''
    import subprocess,os
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)

def main():
    '''Function prints the main interface of the program.'''
    cls()
    print("HABITS TRACKER!\n")

    print('(1) Current Habits:')
    print('(2) Add New Habit\n(3) View All Habits\n(4) My Progress')

    print('\n-type \'h\' for help. \'q\' to quit.')


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
        print('add new habit help')

    elif interface == 'view all habits':
        print('to go back, type "main"')
        print('view all habits help')

    elif interface == 'my progress':
        print('to go back, type "main"')
        print('my progress help')

    

def current_habits():

    #clear screen to show sub-menu interface
    cls()
    print('CURRENT HABITS:\n')
    print('(1) Walking | Duration: 0h:17m | 3')
    print('(2) Newspaper | Duration: 1h:17m | 8')
    print('(3) Cat feed | Coming up: 7h:3m | 6')
    print('\nto go back, type "main"')


def add_new_habit():
    '''add_new_habit is a function that adds new habit
       and stores it in the database.

       It prompts the user to enter three inputs; title,
       description and duration.'''

    #clear screen to show sub-menu interface
    cls()
    
    #define a variable to control the conditional statement
    confirm = 'n'

    #define while loop so in case user enters wrong info
    #they can fix it by repeating steps
    while True:
        if confirm == 'n':
            print('ADD NEW HABIT:\n')
            print("You can enter 'title', 'description' and 'duration' for your new habit.")
            print('To cancel habit entry, leave all fields empty.')
            title = input('>> Title: ')
            description = input('>> Description: ')
            duration = input('>> Duration: ')

            #define a way to cancel new habit entry
            #due to simplicity of CLI, leaving empty fields
            #should indicate to the program that habit entry
            #is cancelled.
            if title + description + duration == '':
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
    
