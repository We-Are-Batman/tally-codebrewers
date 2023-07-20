import tkinter as tk
from tkinter import ttk
import win32api
import psutil

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
        
        drive_button = tk.Button(root, text=drive_info, bg="#f0f0f0", fg="#000000",font=("Helvetica", 10, "bold"),width=20)
        drive_button.pack(pady=5)


root = tk.Tk()
root.title("Disk Space Manager")
root.geometry("600x400")
root.configure(bg="#93a8f5")
s = ttk.Style()
s.theme_use('winnative')

show_disk_usage()

root.mainloop()
