from functions import *

main()

interface = 'main'

while True:
    user = input('>> ')
    if user=='h':
        help(interface)
        
    elif user=='q':
        quit()

    elif user=='main':
        main()
        interface = 'main'
        
    elif user=='1' or user.lower() == "Current Habits".lower():
        current_habits()
        interface = 'current habits'
        
    elif user=='2' or user.lower() == 'Add New Habit':
        add_new_habit()
        interface = 'add new habit'
        
    elif user=='3' or user.lower() == 'View All Habits'.lower():
        view_habits()
        interface = 'view all habits'
        
    elif user=='4' or user.lower() == 'My Progress'.lower():
        progress()
        interface = 'my progress'
