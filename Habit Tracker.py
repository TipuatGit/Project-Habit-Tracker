from functions import *

print("HABITS TRACKER!\n")

print('(1) Current Habits:')
print('''

''')
print('(2) Add New Habit\n(3) View All Habits\n(4) My Progress')

print('\n-type \'h\' for help. \'q\' to quit.')


def progress():
    print('prog works!')

while True:
    user = input('>> ')
    if user=='h':
        help()
        
    elif user=='q':
        close()
        
    elif user=='1' or user.lower() == "Current Habits".lower():
        current_habits()
    elif user=='2' or user.lower() == 'Add New Habit':
        add_new_habit()
    elif user=='3' or user.lower() == 'View All Habits'.lower():
        view_habits()
    elif user=='4' or user.lower() == 'My Progress'.lower():
        progress()
