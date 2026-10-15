import pandas as pd
import tkinter as tk
from tkinter import ttk

def get_file():
    # loads in data file
    print("Find Daily High and Low temp.\n")

#    for debugging
    file_name = "weather_data.txt"

#    file_name = input("Enter the file name: ")

    if file_name[-4:] != ".txt":
        file_name += ".txt"


    raw_file = pd.read_csv(file_name)

    return raw_file


def get_possible_dates(raw_file):
    possible_dates = raw_file['Date'].drop_duplicates().tolist()

    return possible_dates

def cull_data_set(raw_file, date):
    culled_data_set = raw_file[(raw_file['Date'] == date)]

    return culled_data_set

def find_min_max(raw_file):
    date = selected_date.get()
    culled_data_set = cull_data_set(raw_file, date)
    max = str(culled_data_set[" Outdoor temperature (ºF)"].max())
    min = str(culled_data_set[" Outdoor temperature (ºF)"].min())

#    min.set(min)
#    max.set(max)

    print("Max temperature: ", max)
    print("Min temperature: ", min)

    pass


# load in file and pull possible dates for dropdown list
raw_file = get_file()
possible_dates = get_possible_dates(raw_file)

# GUI formatting
root = tk.Tk()
root.geometry("500x500")
root.title("Find the daily min and max temperature!")
root.configure(background="#1b1b1b")
# Label & combobox formatting
style = ttk.Style()
style.configure("Dark.Label", background="#1b1b1b", foreground="#E7E7E7")

# user variables
selected_date = tk.StringVar()
# min = tk.StringVar()
# max = tk.StringVar()

date_label = ttk.Label(root, text="Select Date:", style="Dark.Label")
date_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
date_combo = ttk.Combobox(root, textvariable=selected_date, state="readonly")
date_combo['values'] = possible_dates
date_combo.current(0)
date_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

'''
Isn't currently working...

min_label = ttk.Label(root, text="Minimum Temperature:", style="Dark.Label", textvariable=min)
max_label = ttk.Label(root, text="Maximum Temperature:", style="Dark.Label", textvariable=max)
'''

btn = tk.Button(root, text="Find Daily High and Low", command=lambda: find_min_max(raw_file))
btn.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

root.mainloop()
