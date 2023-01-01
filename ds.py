# Display statistics function

def display_stats():
    # files to read
    task_file_to_read = 'task_overview.txt'
    user_file_to_read = 'user_overview.txt'
    
    #Start of code for reading 'task_overview.txt'
    # open the task file, readlines and strip \n chars
    with open(task_file_to_read) as t_file:
        lines = t_file.readlines()
    
    # print the contents
    print('\n-------------------------------------------------------\n')
    print('\nTasks Overview\n')    
    for line in lines:
        print(line)
    # End of code for reading 'task_overview.txt'
    
    
    #Start of code for reading 'user_overview.txt'
    # open the task file, readlines and strip \n chars
    with open(user_file_to_read) as u_file:
        lines = u_file.readlines()
    
    print('\n-------------------------------------------------------')
    # print the contents
    print('\nUser Overview\n')    
    for line in lines:
        print(line)
    
    print('\n-------------------------------------------------------')
    # End of code for reading 'user_overview.txt'

# End of display_stats() function