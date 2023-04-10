from functions import *

main()

while True:
    user = input('>> ')
    if user=='h':
        help()
        
    elif user=='q':
        quit()
        
    elif user=='1' or user.lower() == "Current Habits".lower():
        current_habits()
                
    elif user=='2' or user.lower() == 'Add New Habit':
        add_new_habit()
        
    elif user=='3' or user.lower() == 'View All Habits'.lower():
        view_all_habits()
        
    elif user=='4' or user.lower() == 'My Progress'.lower():
        my_progress()
