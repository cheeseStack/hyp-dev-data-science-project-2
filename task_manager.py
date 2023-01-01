# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

# to do:
# Create and/or modify the following functions:
    # reg_user - called when user enteres 'r'. Modify to ensure no duplicate usernames, providing relevant message a retry if needed. Perhaps a while loop for while user_entry in [usernames] list, give error message and ask for new username
    # add_task for when user enteres 'a' 
    # view_all for when user enter 'va' to view the tasks in 'tasks.txt'
    # view_mine for when user enters 'vm'. Modify to display tasks as an ordered numbered list; allow user to select a specific task by its number (enumerate); mark as complete or edit task to assign to different username or different due date.
    # add generate_reports for when user selects 'gr'. See the brief for full details to include.
    # NOTE that any commmented-out print statements were for testing purposes.
    
#=====importing libraries===========
import os
from datetime import datetime, date
# ds.py file for the display_stats() function
from ds import display_stats

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    curr_pass = input("Password: ")
    if username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


## Define the functions that depend on the tasks.txt and user.txt data

# Start of reg_user function
'''reg_user - Add a new user to the user.txt file'''
def reg_user():
    # - Request input of a new username
    new_username = input("New Username: ")
    
    # REQUIRED MODIFICATION: while loop to request a unique username if existing one is selected, then continue to request a new password
    while new_username in username_password.keys():
        new_username = input('That username is taken - please select another username.\nNew Username: ')
    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
        
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
 
    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")
# End of reg_user function
    
    
# Start of add_task function   
def add_task():
    '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
             
    task_username = input("Name of person assigned to task: ")
    while task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        task_username = input("Name of person assigned to task: ")
        continue
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")
# End of add_task function


# Start of view_all function
def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)
# End of view_all function


# Start of view_mine function
def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
    # while loop to show the tasks with just the task number and title, such as
    '''Task 1: Name of task         Completed?: Yes or No'''
    # This code allows the user to change from complete to not complete, in case it is marked complete in error, or needs to be redone or reassigned
    # Ask the user to select the task number, or -1 to exit to the main menu, and alert if task number selected in not valid.

    while True:
         # empty index list to add to below, for conditional checking in while loop in next block of code
        indices = []
        # Show abbreviated list of available tasks
        print('Your tasks:')
        for index, t in enumerate(task_list):
            # only show incomplete tasks
            if t['username'] == curr_user:
                indices.append(index+1) # add to indices list
                compl = "Yes" if t['completed'] else "No"
                message = f"\tTask {index+1}: {t['title']}. \tCompleted?: {compl} "
                print(message)
        try:
            selection = int(input("Enter the task number for more details ('-1' for main menu): "))
        except ValueError: # error handling in case characters are entered instead of numbers
            print('Invalid selection - enter numbers only.')
            continue
        if selection == -1: # exit to the main menu
                break
        elif selection not in indices:
            print('Task number not valid.')
            continue # loops around again if invalid input
        for index, t in enumerate(task_list):
            if selection == index+1:
                disp_str = f'Task number: \t {index+1}\n'
                disp_str += f"Task: \t\t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                comp = 'Yes' if True else 'No'
                disp_str += f"Completed? \t {comp}"
                print(disp_str)
                
                # Add options to MARK AS COMPLETE or EDIT TASK (change user or due date)
                # Option to mark as complete or change from complete to not complete and reassign / change due date
                print("\nDo you want to mark or keep this task as complete?")
                while True:
                    complete = input("Enter 'Yes' or 'No': ").lower()
                    if complete == 'yes':
                        t['completed'] = True
                        print(f'You have marked task {index+1} as complete.')
                        break
                    elif complete == 'no':
                        t['completed'] = False
                        print(f'Task number {index+1} is still outstandding.')  
                        break
                    else:
                        print('Invalid input.')
                        continue
                
                    # Ask the user if they want to edit the task's user or due date if the task is not complete
                if t['completed'] == False:    
                    print('\nDo you want to assign this task to a differnt user?')
                    while True:
                        diff_user = input("Enter 'Yes' or 'No': ").lower()
                        if diff_user == 'yes':
                            message = 'Which user do you want to assign this task to?'
                            # display users except current user
                            for user in username_password.keys():
                                if user != curr_user:
                                    message += f'\n\t{user.title()}'
                            print(message)
                            user_assigned = input(': ')
                            if user_assigned not in username_password.keys():
                                print('Username not recognised')
                            t['username'] =  user_assigned
                            print(f'You have asssigned this task to {user_assigned.title()}.')  
                            break
                        elif diff_user == 'no':
                            print('You are still responsible for this task.')
                            break
                        else:
                            print('Invalid input.')
                            continue  
                    
                # As the user if they want to change to due date if not completed
                if t['completed'] == False:
                    print(f"\nDo you want to change the due date from {t['due_date'].strftime(DATETIME_STRING_FORMAT)} ?")
                    while True:
                        change_due_date = input("Enter 'Yes' or 'No': ").lower()
                        # if YES
                        if change_due_date == 'yes':
                            # change due date, copying the error handling method from the add_task element.
                            try:
                                new_due_date = input("Due date of task (YYYY-MM-DD): ")
                                new_due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                                t['due_date'] = new_due_date_time
                                print(f"You have changed the due date to {t['due_date']}")
                                break

                            except ValueError:
                                print("Invalid datetime format. Please use the format specified")
                        # if NO       
                        if change_due_date == 'no':
                            print(f"You have kept the due date as {t['due_date']}")
                            break
                        # if invalid input   
                        else: 
                            print('Invalid input.')
                            continue           
        
            ''' Write the amended information to the tasks.txt file'''
            # This updates all tasks with any of the changes made above
            with open("tasks.txt", "w") as task_file:
                task_list_to_write = []
                for t in task_list:
                    str_attrs = [
                        t['username'],
                        t['title'],
                        t['description'],
                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                        "Yes" if t['completed'] else "No"
                    ]
                    task_list_to_write.append(";".join(str_attrs))
                task_file.write("\n".join(task_list_to_write))
        print("Tasks have been updated in the tasks.txt file.")
   
# End of view_mine function               
    
    
# Start of gen_reps (generate reports) function
# NOTE: commented-out print statements are for testing only
def gen_reps():
    ''' task_overview.txt contents'''
    # total number of tasks generated and tracked in task_manager.py: length of task_list
    total_tasks = len(task_list)
    # print(total_tasks)
    
    # total number of completed tasks: tasks where ['completed'] == True
    total_completed_tasks = 0
    for task in task_list:
        if task['completed'] == True:
            total_completed_tasks += 1
    # print(total_completed_tasks)
    
    # total number of UNcompleted tasks: tasks where ['completed'] == False
    total_uncomplete_tasks = 0
    for task in task_list:
        if task['completed'] == False:
            total_uncomplete_tasks += 1
    # print(total_uncomplete_tasks)
    
    # total number of uncomplete overdue tasks
    total_overdue_uncomplete = 0
    for task in task_list:
        # check if incomplete and due date is less (or earlier) than today's date
        if task['completed'] == False and task['due_date'] < datetime.today():
            total_overdue_uncomplete += 1
    # print(total_overdue_uncomplete)
    
    # % of uncomplete tasks, rounded to nearest whole number:
    pc_uncomplete = round(total_uncomplete_tasks / total_tasks * 100)
    # print(pc_uncomplete)
    
    # % of overdue (uncomplete) tasks
    pc_overdue = round(total_overdue_uncomplete / total_tasks * 100)
    # print(pc_overdue)
    
    # message to write
    task_message = f'Total number of generated and tracked tasks: {total_tasks}\n'
    task_message += f'Total number of completed tasks: {total_completed_tasks}\n'
    task_message += f'Total number of uncompleted (outstanding) tasks: {total_uncomplete_tasks}\n'
    task_message += f'Total number of uncompleted, overdue tasks: {total_overdue_uncomplete}\n'
    task_message += f'Percentage of uncompleted tasks: {pc_uncomplete}%\n'
    task_message += f'Percentage of overdue, uncompleted tasks: {pc_overdue}%\n'
    
    # write to file and give user notification
    file_to_write = 'task_overview.txt'
    with open(file_to_write, 'w') as t_file:
        t_file.write(task_message)
    print(f'The file {file_to_write} has been been created.')
    
    
    # gen_reps() user overview
    ''' user_overview.txt contents'''
    # total number of registered users will be generated at the time of writing the txt file
    
    # total tasks as per task_overview.txt: use 'total_tasks' variable 
    
    # For each user display:
        # no. assigned tasks
        # % assigned of total globally
        # % completed of assigned
        # % uncompleted assigned
        # % overdue uncompleted
    users_list = []
    for user in username_password.keys():
        users_list.append(user)
    users_list_sorted = sorted(users_list)
    # print(users_list_sorted)
    
    # count assigned tasks
    assigned_tasks = {}
    for user in users_list_sorted:
        for task in task_list:
            if task['username'] == user:
                assigned_tasks[user] = assigned_tasks.get(user, 0) + 1
                
    # user with no assigned tasks
    no_task_users = []
    for user in users_list_sorted:
        if user not in assigned_tasks.keys():
            no_task_users.append(user)
    # print(no_task_users) 
       
    # print('Assigned tasks')
    # print(assigned_tasks)
    
    # % assigned of total globally, to 2dp
    # divide assigned tasks by total global tasks for each user
    pc_assigned = {}
    for key, value in assigned_tasks.items():
        pc_assigned_val = round((value / total_tasks * 100), 2)
        pc_assigned[key] = pc_assigned_val
    # print('percentage assigned of total')
    # print(pc_assigned)   
    
    # % completed of assigned and % uncompleted
    number_completed = {}
    pc_completed = {}
    
    number_uncompleted = {}
    pc_uncompleted = {}
    
    # get the number of completed and uncompleted tasks
    for user in users_list_sorted:
        for task in task_list:
            # Completed tasks
            if task['username'] == user and task['completed'] == True:
                number_completed[user] = number_completed.get(user, 0) + 1
  
    # get the number of completed and uncompleted tasks
    for user in users_list_sorted:
        for task in task_list:
            # UNcompleted tasks
            if task['username'] == user and task['completed'] == False:
                number_uncompleted[user] = number_uncompleted.get(user, 0) + 1
            
    # print('number completed')
    # print(number_completed)
    # print('number UNcompleted')
    # print(number_uncompleted)
    # Use the above obtained values to find the respective percentages
    # Percentage Completed
    for key, value in number_completed.items():
        for k, v in assigned_tasks.items():
            if key == k:
                pc_comp_val = round((value / v * 100), 2)
                pc_completed[key] = pc_comp_val     
    # print(' Percentage Completed')
    # print(pc_completed)
    
     # Percentage UNcompleted
    for key, value in number_uncompleted.items():
        for k, v in assigned_tasks.items():
            if key == k:
                pc_uncomp_val = round((value / v * 100), 2)
                pc_uncompleted[key] = pc_uncomp_val
    # print(' Percentage UNcompleted')
    # print(pc_uncompleted)
   
    # % overdue uncompleted
    number_overdue_uncompleted = {}
    pc_overdue_uncompleted = {}
    
    # Find the number overdue of each user
    for user in users_list_sorted:
        for task in task_list:
            # UNcompleted and overdue tasks
            if task['username'] == user and task['completed'] == False and task['due_date'] < datetime.today():
                number_overdue_uncompleted[user] = number_overdue_uncompleted.get(user, 0) + 1
    #  add a zero value to those without any overdue tasks(is there a way of doing it above??)
    for user in assigned_tasks.keys():
        if user not in number_overdue_uncompleted.keys():
            number_overdue_uncompleted[user] = 0
    # print('number overdue uncompleted')
    # print(number_overdue_uncompleted)
    
    # find % overdue uncomplete
    for key, value in number_overdue_uncompleted.items():
        for k, v in assigned_tasks.items():
            if key == k:
                pc_overdue_val = round((value / v * 100), 2)
                pc_overdue_uncompleted[key] = pc_overdue_val
    # print('percentatage overdue incomplete')
    # print(pc_overdue_uncompleted)
    
    ''' Next use the .get() method to obtain the key for each user in users_list_sorted to display in a user friendly way'''
    ''' Export into user_over_view.txt'''
    # make a dictionary for each user, storing the information above in a list0
    # print('user overviews')
    user_overview_list = [] # to store the dictionaries of user details
    message_list = [] # this will be writtem to the user_overview.txt file
    for user in users_list_sorted:
        user_overview = {} # this may be redundant, but could be used to store the data of all users for reference.
        user_overview['name'] = user
        user_overview['tasks'] = assigned_tasks.get(user, value)
        user_overview['percentage_assigned'] = pc_assigned.get(user, value)
        user_overview['percentage_completed'] = pc_completed.get(user, value)
        user_overview['percentage_uncompleted'] = pc_uncompleted.get(user, value)
        user_overview['percentage_overdue'] = pc_overdue_uncompleted.get(user, value)  
        # print(user_overview)
        
        # write the elements here to the file
        user_message =  f'Username: {user}\n'
        user_message += f'Number of tasks assigned: {assigned_tasks.get(user, value)}\n'
        user_message += f'Assigned tasks as a percentage of all tasks : {pc_assigned.get(user, value)}%\n'
        user_message += f'Percentage of tasks completed: {pc_completed.get(user, value)}%\n'
        user_message += f'Percentage of tasks uncompleted: {pc_uncompleted.get(user, value)}%\n'
        user_message += f'Percentage of tasks overdue: {pc_overdue_uncompleted.get(user, value)}%\n'
        message_list.append(user_message)
        user_overview_list.append(user_overview)
    # print('user_overview_list')
    # print(user_overview_list)
    # print('Message List:')
    # print(message_list)
        
    # ''' Reports are then read from task_overview.txt and user_overview.txt to display on screen
    # cycle through the user_overview_list for each user_overview and output in a readable way to be written to the .txt file.
    # num users and num tasks from ds code
    num_users_message = f'Number of registered users: {len(username_password.keys())}'
    num_tasks_message = f'Number of tasks generated: {len(task_list)}'
    user_file_to_write = 'user_overview.txt'
    with open(user_file_to_write, 'w') as u_file:
        u_file.write(num_users_message + '\n' + num_tasks_message + '\n\n' + '\n'.join(message_list))
       
    print('user_overview.txt file created.')
   

        
        
# Start of user entry after logging in
# show the gr (generate reports) option for admins only
while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    if curr_user == 'admin':
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    ds - Display statistics
    e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    ds - Display statistics
    e - Exit
    : ''').lower()

    if menu == 'r':
        # call the reg_user function
        reg_user()
    
    elif menu == 'a':
        # call the add_task function
        add_task()
        
    elif menu == 'va':
        # call the view_all function
        view_all()
        
    elif menu == 'vm':
        # call the view_mine function
        view_mine()
        
    # add the option gr: generate reports, for admins only
    elif menu == 'gr' and curr_user == 'admin':
        # call the gen_reps functions
        gen_reps()
    
    # Modify yhr ds menu option to read reports from the task_overview.txt and user_overview.txt filesd      
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        # comment out the original stats and use the display_stats() function
        # num_users = len(username_password.keys())
        # num_tasks = len(task_list)

        # print("-----------------------------------")
        # print(f"Number of users: \t\t {num_users}")
        # print(f"Number of tasks: \t\t {num_tasks}")
        # print("-----------------------------------") 
        # generate reports if they do not exist
        gen_reps()  
        display_stats() 

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")   