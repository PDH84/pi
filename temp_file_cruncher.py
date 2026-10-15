"""
Probably obsolete.
12/1/23
"""
import os
import csv

path = "./templogger"
dir_list = os.listdir(path)     # creates a list of all files in directory
dir_list.sort()                 # sorts them into ascending order
new_list = []

for f in dir_list:
    new_row = []
    file = open('{0}/{1}'.format(path, str(f)), 'r')
    new_row.append(f)
    file_dump = file.read()
    temp = file_dump[:4]
    humid = file_dump[5:]
    new_row.append(temp)
    new_row.append(humid)
    file.close()
    new_list.append(new_row)

print(new_list)
final_file = open('temp_logger.csv', 'w', newline='')

with final_file:
    write = csv.writer(final_file)
    write.writerows(new_list)
