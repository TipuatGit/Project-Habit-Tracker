def close():
    pass

def help():
    if interface == 'main':
        print('''\nWelcome to HABITS TRACKER!
        How to navigate around the program:

        ''')

    elif interface == 'current habits':
        print('current habits help')

    elif interface == 'add new habit':
        print('add new habit help')

    elif interface == 'view all habits':
        print('view all habits help')

    elif interface == 'my progress':
        print('my progress help')

    

def current_habits():
    print('current_habits works!')

def add_new_habit():
    print('add_new_habit works!')

def view_habits():
    print('view_habits works!')
