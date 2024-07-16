'''
Recives the sub-task from memory or interpreted user interface(W.I.P) and executes the command.
i.e. "Grab the apple" is read or recived as "grab" and "apple" as objective and object. "grab"
command is executed on the object "apple".

Needs a logic block for checking if a sub-task is repeatble or needs repeating before it is complete  
'''
# import rospy
import time
import os
import json
# from temp_object_memory import scan_enviroment


subtasks = [
    "Pick a cereal bowl",
    "Pour cereal in bowl",
    "Pick milk bottle",
    "Pour milk in bowl",
    "Pick spoon",
    "Place spoon in bowl"
]
current_subtask_index = 0

def start():
    global current_subtask_index
    current_subtask_index = 0

def stop():
    pass

def reset():
    global current_subtask_index
    current_subtask_index = 0

def pause():
    pass

def next_subtask():
    global current_subtask_index
    if current_subtask_index < len(subtasks) - 1:
        current_subtask_index += 1

def get_subtasks():
    return subtasks, current_subtask_index

def previous_subtask():
    global current_subtask_index
    if current_subtask_index > 0:
        current_subtask_index -= 1

# ------------------------------------------------------- /// Functions
def update_tasks():
    ''' reads the physical memory location to load previously defined
        tasks, sub-tasks and basic actions.'''
    
    global tasks, action_list
    tasks =[]
    for task in os.listdir("tasks/"):
        if task.endswith(".json"):
            tasks.append(task[:-5])

    action_list = ['move','grip','end','test'] + tasks
 
def run_task(task_name, task_targets, depth):
    ''' loads a previously recorded task file and runs through the chain of commands'''

    global current_depth # defines whether a task is within another task, or effctively a sub-task. 0 defines a task and higher numbers mean sub-task.
    current_depth = depth
    task_file = "tasks/" + task_name + '.json'
    with open(task_file, 'r') as file:  
        sub_tasks = json.load(file) # loads the chain of commands

    if sub_tasks[0][0] == 'general': 
        # [0][0] in the json file indicates whether a task is customizable or not.
        # if the task is customizable, [0][1] indicates which items can be changed.

        if current_depth == 0: 
            # asks the user if they want to change the replacable items/targets within the chain of commands

            task_targets = []
            print( len(sub_tasks[0][1]), " changable parameters were found, these parametes are:\n", sub_tasks[0][1] ) 
            if yes_no_question("do you want to change these parameters? y/n:") :
                while len(task_targets) != len(sub_tasks[0][1]):
                    task_targets = raw_input("Please enter a new set of parameters , separate them with space:").lower().split()
                general_task_mod(sub_tasks, task_targets)
        
        elif task_targets != sub_tasks[0][1]: 
            # if the depth is not zero, the task is being run as a sub task
            # will automatically replace the items in general sub task if
            # required.

            general_task_mod(sub_tasks, task_targets)
    
    current_depth += 1   
    for action in sub_tasks[1:]: # executes actions from chain of command
        
        run_sub_task(action[0],action[1])
        time.sleep(1)


def run_sub_task(action_name,target_name):
    ''' executes sub-tasks (as tasks) and basic actions '''

    if action_name in tasks: # Runs if the action is a previously recorded task
        
        run_task(action_name, target_name, current_depth)

    else: # Runs if the action is a hardcoded basic action

        # action target can be an object, a direction or a rotation depending on action
        # W.I.P : LLM processing should be able to verify wether the target type is correct                
        task_command = "basic_actions" + "." +  action_name
        __import__(task_command, fromlist=['']).action(target_name, memory, []) # third input is the interaction mode or direction, should be defined later.

def general_task_mod(sub_tasks, task_targets):
    '''replaces all mentions of an items in item_set1, within a chain of commands, to items in item_set1.'''

    # needs to be improved for GUI to allow the user to see which items are being changed to what
    # and to be able to manually replace items
    count = 0
    for item in sub_tasks[0][1]:

        for i in range(len(sub_tasks[1:])):
            if isinstance(sub_tasks[i+1][1], list):
                sub_tasks[i+1][1] = [object.replace(item,task_targets[count]) for object in sub_tasks[i+1][1]]
            else:
                if sub_tasks[i+1][1] == item:
                    sub_tasks[i+1][1] = task_targets[count]

        count +=1

    return sub_tasks

def yes_no_question(text):
    '''temporary, will be removed when GUI is here.'''

    while True:
        txt_input = raw_input(text).lower()
        if txt_input == "y" or txt_input == "yes" :
            return True
        elif txt_input == "n" or txt_input == "no":
            return False    
        else:
            print("Wrong format, please try again")

# # ------------------------------------------------------- /// ROS             
# rospy.init_node('random_name_node', anonymous=True)# find a better name for node, cause why not
# rate = rospy.Rate(20)

# ------------------------------------------------------- /// Main
# while not rospy.is_shutdown():

#     update_tasks()
#     memory = scan_enviroment()
#     print (memory)# sanity check
#     task_name = raw_input("please enter task name: ")
    
#     if task_name in tasks: # runs the task if it has been previously defined
        
#         run_task(task_name,[], 0)
        
#         print( "task complete?")
        
#     else: # defines new task 

#         print("Tasks that can be repeated in the exact same manner on \ndifferent objects, just by replacing targets, are called general tasks")
#         sub_tasks = []
        
#         if yes_no_question("Is this a general task? y/n:") : # categorizes task for future runs
#             task_targets = raw_input("Please enter all changable objects, separate them with space:").lower().split()
#             sub_tasks.append(["general", task_targets])
#         else:
#             sub_tasks.append(["not_general", "N/A"])

#         while True:
#             action_name = raw_input("please enter the action(i.e move, end) :").lower()

#             if action_name == 'end': # 'end' command ends the task and saves the chain of commands
#                 break

#             elif action_name not in action_list: 
#                 # should create a new task/sub task. might need to turn the section after else(define new task)
#                 # into a function and run it within itself for this section.
#                 print('Action is not defined')
#                 print('this section is WIP, please select a predefind action or task')
#                 print('predefined actions are: ', action_list)
#                 continue

#             if action_name in tasks: 
                    
#                 task_file_temp = "tasks/" + action_name + '.json'     
#                 with open(task_file_temp, 'r') as file:  
#                     temp_sub_tasks = json.load(file)          
                
#                 if temp_sub_tasks[0][0] == 'general':
#                     print( len(temp_sub_tasks[0][1]), " changable parameters were found for this sub-task, these parametes are:\n", temp_sub_tasks[0][1] ) 
#                     if yes_no_question("do you want to change these parameters? y/n:") :
#                         target_name =[]
#                         while len(target_name) != len(temp_sub_tasks[0][1]):
#                             target_name = raw_input("Please enter a new set of parameters , separate them with space:").lower().split()
#                     else: 
#                         # adds the sub-task to task with modifiable targets
#                         # in the gui user should have the option to add the sub task
#                         # and set the targets as unmodifiable within a task.
#                         target_name = temp_sub_tasks[0][1]

#                 else:
#                     target_name = "N/A"
#             else:
#                 # action target can be an object, a direction or a rotation depending on action
#                 # W.I.P : LLM processing should be able to verify wether the target type is correct
#                 target_name = raw_input("please enter action target: ").lower()
            
             
#             try:
#                 run_sub_task(action_name,target_name) # runs the sub task
#                 sub_tasks.append([action_name, target_name]) # updates the chain of command
#             except:
#                 print("well that didn't work.\n action was not saved as part of sub-task.")

#         # saves the chain of commands after reciving the "end" command
#         task_file = "tasks/" + task_name + '.json'
#         with open(task_file, "w") as file:
#             json.dump(sub_tasks, file) 
