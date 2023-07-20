import os
import json
import concurrent.futures
import tkinter as tk
from tkinter import ttk
from functools import partial
import psutil
import win32api

# Read from json file into dictionary
with open('file_association.json') as json_file:
    extensions = json.load(json_file)

def process_file(file_path):
    try:
        file_stats = os.stat(file_path)
    except:
        return

    split_tup = os.path.splitext(file_path)
    file_extension = split_tup[1]
    if len(file_extension) < 1:
        return

    actual_type = extensions.get(file_extension, "documents")
    return actual_type, file_stats.st_size

def get_files_and_metadata(drive):
    file_dict = {}
    breakdown_by_type = {}

    for root, _, files in os.walk(drive):
        for filename in files:
            file_path = os.path.join(root, filename)
            result = process_file(file_path)
            if result is not None:
                actual_type, size = result
                if actual_type not in file_dict:
                    file_dict[actual_type] = 0

                file_dict[actual_type] += size

                breakdown_by_type.setdefault(actual_type, []).append(file_path)

    return file_dict, breakdown_by_type

def show_breakdown(drive, file_dict, breakdown_by_type):
    show_breakdown_window = tk.Toplevel(root)
    show_breakdown_window.title(f"Drive {drive[:2]} Usage Breakdown")
    show_breakdown_window.geometry("600x400")
    show_breakdown_window.config(bg="#93a8f5")

    drive_info = f"Drive: {drive}\n"
    for extension, size in file_dict.items():
        tot = float("{:.2f}".format(size / (1024.0)))
        drive_info += f"{extension}: {tot} KB\n"

    drive_label = tk.Label(show_breakdown_window, text=drive_info, bg="#93a8f5", fg="#000000", font=("Helvetica", 10, "bold"))
    drive_label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

    for idx, (file_type, file_list) in enumerate(breakdown_by_type.items(), 1):
        file_type_label = tk.Label(show_breakdown_window, text=f"{file_type} Files:", bg="#93a8f5", fg="#000000", font=("Helvetica", 10, "bold"))
        file_type_label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

        file_list_text = "\n".join(file_list)
        file_list_label = tk.Label(show_breakdown_window, text=file_list_text, bg="#f0f0f0", fg="#000000", font=("Helvetica", 8), justify="left", anchor="w", wraplength=500)
        file_list_label.grid(row=idx, column=1, padx=10, pady=5)

def show_disk_usage():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]

    for drive in drives:
        drive_label = drive[:2]
        obj_Disk = psutil.disk_usage(drive)
        total_gb = float("{:.2f}".format(obj_Disk.total / (1024.0 ** 3)))
        used_gb = float("{:.2f}".format(obj_Disk.used / (1024.0 ** 3)))
        free_gb = float("{:.2f}".format(obj_Disk.free / (1024.0 ** 3)))
        free_percent = float("{:.2f}".format(obj_Disk.percent))

        drive_info = f"Drive: {drive_label}\nTotal: {total_gb} GB\nUsed: {used_gb} GB\nFree: {free_gb} GB\nFree %: {free_percent}"

        drive_button = tk.Button(root, text=drive_info, bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=40,
                                 command=partial(drive_specific, drive))
        drive_button.pack(pady=5)

def drive_specific(drive):
    file_dict, breakdown_by_type = get_files_and_metadata(drive)
    show_breakdown(drive, file_dict, breakdown_by_type)

root = tk.Tk()
root.title("Disk Space Manager")
root.geometry("600x400")
root.configure(bg="#93a8f5")
s = ttk.Style()
s.theme_use('winnative')

show_disk_usage()

root.mainloop()
