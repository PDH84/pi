from datetime import datetime


def determine_schedule_status(mesh_message_first, time_between_messages):
    initial_msg_time = datetime.strftime(mesh_message_first, "%H:%M")



    return initial_msg_time
'''
+----------------------+-------------------------------------------------------+
|Meshcore weather      | Type in first time to send message (24hr format)      |
|message send          | Then put in how many hours between messages (in hours)|
|schedule              |                                                       |
+----------------------+-------------------------------------------------------+
'''
mesh_message_first = "3:00"
time_between_messages = 3

initial_msg_time = determine_schedule_status(mesh_message_first, time_between_messages)

print(initial_msg_time)
