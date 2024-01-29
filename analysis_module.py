from tabulate import tabulate

#define function to calculate habit streaks and missed tasks
def habit_analysis(user_input, habits_table, streak):
    habits = [] #define list to store habits
    count = 0 #define variable to make index for habits in table
    index_to_id = {} #define dict to convert between habit id and display index
    longest_streak = {} # store all streaks of a habit

    #add habits to the list
    for row in habits_table:
        
        if row[5] == user_input:
            count += 1
            index_to_id.setdefault(count, row[0])
            tasks = sum(streak.get(row[0],[]))
            total_tasks = len(streak.get(row[0],[]))
            habits.append([count, row[1], str(tasks) + '/' + str(total_tasks)])
    
    #calculate all streaks for each habit, includes both streaks and missed days
    for id in index_to_id:
        longest_streak.setdefault(index_to_id[id], [])
        ones_sum = 0
        zeros_sum = 0

        try:
            for task_count in streak[index_to_id[id]]:
                if task_count == 1:
                    ones_sum += 1
                elif ones_sum >0:
                    longest_streak[index_to_id[id]].append(ones_sum)
                    ones_sum = 0

                if task_count == 0:
                    zeros_sum += 1
                elif zeros_sum > 0:
                    longest_streak[index_to_id[id]].append(-zeros_sum)
                    zeros_sum = 0

            if ones_sum > 0:
                longest_streak[index_to_id[id]].append(ones_sum)
            if zeros_sum > 0:
                longest_streak[index_to_id[id]].append(-zeros_sum)

        except KeyError:
            continue

    #add streaks to habits list
    for row in habits:
        max_streak = max(longest_streak[index_to_id[row[0]]], default=0)
        row.append(max_streak) if max_streak > 0 else row.append(0)

    #display the habits in table
    print(tabulate(habits, headers=['', 'Daily Habits', 'Tasks Completed', 'Max Streak'], tablefmt='orgtbl'))

    return habits, longest_streak, index_to_id
