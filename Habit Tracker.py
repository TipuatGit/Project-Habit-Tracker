from functions import *


main()

while True:
    
    current_time = datetime.datetime.now().time()

    habits_table, _ = get_data()

    for (id, title, desc, start, end, type, date) in habits_table:
        end_time = datetime.datetime.strptime(end, '%H:%M:%S').time()
        
        if current_time > end_time:
            connection = sqlite3.connect('habit_db TEST.db')
            cursor = connection.cursor()
            
            # Check the habit type before entering 0 for missed habits
            if type == 'daily':
                query = "SELECT * FROM task_completion WHERE habit_id = ? AND DATE(completion_time) = DATE(?)"
                cursor.execute(query, (id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                existing_record = cursor.fetchone()
                
                if not existing_record:
                    query = "INSERT INTO task_completion (habit_id, completion_status, completion_time) VALUES (?,?,?)"
                    cursor.execute(query, (id, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    connection.commit()
            
            elif type == 'weekly':
                query = "SELECT * FROM task_completion WHERE habit_id = ? AND strftime('%W', completion_time) = strftime('%W', ?)"
                cursor.execute(query, (id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                existing_record = cursor.fetchone()
                
                if not existing_record:
                    query = "INSERT INTO task_completion (habit_id, completion_status, completion_time) VALUES (?,?,?)"
                    cursor.execute(query, (id, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    connection.commit()
            
            connection.close()

        
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
