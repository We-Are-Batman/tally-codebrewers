import tkinter as tk
from tkinter import ttk
from functools import partial
import win32api
import psutil
import json
import os

extensions = {}

# Read from JSON file into a dictionary
with open('file_association.json') as json_file:
    extensions = json.load(json_file)

def validate_path(path):
    if os.path.isdir(path):
        pass
    else:
        error_label.config(text="Invalid path. Please enter a valid directory.")

def show_disk_usage(path, ind):
    drive_name = path[:2]
    obj_Disk = psutil.disk_usage(path)
    total_gb = float("{:.2f}".format(obj_Disk.total / (1024.0 ** 3)))
    used_gb = float("{:.2f}".format(obj_Disk.used / (1024.0 ** 3)))
    free_gb = float("{:.2f}".format(obj_Disk.free / (1024.0 ** 3)))
    free_percent = float("{:.2f}".format(obj_Disk.percent))
    
    drive_info = f"Drive: {drive_name}\n Total: {total_gb} GB\nUsed: {used_gb} GB\nFree: {free_gb} GB\nFree %: {free_percent}"
    
    # Add a disabled button to show disk usage
    drive_button = tk.Button(root, text=drive_info, bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=40)
    drive_button.grid(row=ind, column=0, padx=20, pady=10)

root = tk.Tk()
root.title("Disk Space Manager")
# root.geometry("600x400")
root.configure(bg="#93a8f5")
s = ttk.Style()
s.theme_use('winnative')

drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000')[:-1]
row_count = 0
for drive in drives:
    show_disk_usage(drive, row_count)
    row_count += 1

input_path_label = tk.Label(root, text="Enter Path",bg="#93a8f5",font=("Helvetica", 10, "bold"),width=40)
input_path_label.grid(row=row_count, column=0,columnspan=2, padx=20, pady=2)
row_count += 1


input_path_text = tk.StringVar()
input_path_entry = tk.Entry(root, textvariable=input_path_text, width=50)
input_path_entry.grid(row=row_count, column=0, padx=30, pady=5)
row_count += 1

get_insights_btn = tk.Button(root, text="Get Insights", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=40, command=lambda: validate_path(input_path_text.get()))
get_insights_btn.grid(row=row_count, column=0, padx=20, pady=10)

error_label = tk.Label(root, text="", fg="red",bg="#93a8f5")
error_label.grid(row=row_count+1, column=0, padx=20, pady=5)

root.mainloop()
