import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk


def get_file():
    # loads in data file
    print("Welcome to the Wonderful Weather Plotter!\n")
    print("Text block to come...\n\n")

#    for debugging
#    file_name = "weather_data.txt"

    file_name = input("Enter the file name: ")

    if file_name[-4:] != ".txt":
        file_name += ".txt"


    raw_file = pd.read_csv(file_name)

    return raw_file


def get_possible_dates(raw_file):
    possible_dates = raw_file['Date'].drop_duplicates().tolist()

    return possible_dates


def plot_graph(raw_file):
    selected, date_1, date_2 = get_selected()
    culled_data_set = cull_data_set(date_1, date_2, raw_file)
    final_df = culled_data_set[['Date', ' ' + str(selected)]].copy()
    final_df.plot(x=final_df.columns[0], y=final_df.columns[1], kind='line')
    plt.show()

    return None


def get_selected():
    selected = selected_data.get()
    date_1 = start_date.get()
    date_2 = end_date.get()

    return selected, date_1, date_2

def cull_data_set(date_1, date_2, raw_file):
    culled_data_set = raw_file[(raw_file['Date'] >= date_1) & (raw_file['Date'] <= date_2)]

    return culled_data_set

# load in file and pull possible dates for dropdown list
raw_file = get_file()
possible_dates = get_possible_dates(raw_file)

# GUI formatting
root = tk.Tk()
root.geometry("500x500")
root.title("Welcome to the Wonderful Weather Plotter!")
root.configure(background="#1b1b1b")
# Label & combobox formatting
style = ttk.Style()
style.configure("Dark.Label", background="#1b1b1b", foreground="#E7E7E7")

# user input variables
selected_data = tk.StringVar()
start_date = tk.StringVar()
end_date = tk.StringVar()

# labels and combobox
selected_data_label = ttk.Label(root, text="Select Data:", style="Dark.Label")
selected_data_label.pack()
selected_data_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
selected_data_combo = ttk.Combobox(root, textvariable=selected_data, state="readonly")
selected_data_combo['values'] = ("Indoor temperature (ºF)", "Indoor humidity (%)", "Outdoor temperature (ºF)",
                   "Outdoor humidity (%)", "Pressure (hPa)", "Air quality (ohms)")
selected_data_combo.current(0)
selected_data_combo.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

start_date_label = ttk.Label(root, text="Select Date:", style="Dark.Label")
start_date_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
start_date_combo = ttk.Combobox(root, textvariable=start_date, state="readonly")
start_date_combo['values'] = possible_dates
start_date_combo.current(0)
start_date_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

end_date_label = ttk.Label(root, text="Select Date:", style="Dark.Label")
end_date_label.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
end_date_combo = ttk.Combobox(root, textvariable=end_date, state="readonly")
end_date_combo['values'] = possible_dates
end_date_combo.current(0)
end_date_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)


btn = tk.Button(root, text="Plot Weather Data", command=lambda: plot_graph(raw_file))
btn.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

root.mainloop()
