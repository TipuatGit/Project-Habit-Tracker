from functions import *

#check if database exists already
check_database()

#run the main interface of the program
main()

#enter the top-level loop of the program
while True:
    check_missed_habits()
        
    user = input('>> ')
    if user=='h':
        help()
        
    elif user=='q':
        quit()
        
    elif user=='1':
        current_habits()
                
    elif user=='2':
        add_new_habit()
        
    elif user=='3':
        view_all_habits()
        
    elif user=='4':
        my_progress()

    elif user not in ['h', 'q', '1', '2', '3', '4']:
        main()
