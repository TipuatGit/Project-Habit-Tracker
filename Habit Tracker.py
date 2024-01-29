from functions import Functions


#instantiate functions class to properly run the program
#and use all its features
programm = Functions()

#check if database exists already
programm.check_database()

#run the main interface of the program
programm.main()

#enter the top-level loop of the program
while True:
    programm.check_missed_habits()
        
    user = input('>> ')
    if user=='h':
        programm.help()
        
    elif user=='q':
        quit()
        
    elif user=='1':
        programm.current_habits()
                
    elif user=='2':
        programm.add_new_habit()
        
    elif user=='3':
        programm.view_all_habits()
        
    elif user=='4':
        programm.my_progress()

    elif user not in ['h', 'q', '1', '2', '3', '4']:
        programm.main()
