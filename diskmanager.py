import tkinter as tk
from tkinter import ttk
from functools import partial
import win32api
import psutil
import os

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
        
        drive_button = tk.Button(root, text=drive_info, bg="#f0f0f0", fg="#000000",font=("Helvetica", 10, "bold"),width=20,command=partial(drive_specific,drive))
        drive_button.pack(pady=5)

def show_breakdown(drive,root):
    show_breakdown_window = tk.Toplevel(root)
    show_breakdown_window.title(f"Drive {drive} Usage Breakdown")
    show_breakdown_window.geometry("600x400")
    show_breakdown_window.config(bg="#93a8f5")

    drive_label = drive[:2]
    obj_Disk = psutil.disk_usage(drive)
    total_gb = float("{:.2f}".format(obj_Disk.total / (1024.0 ** 3)))
    used_gb = float("{:.2f}".format(obj_Disk.used / (1024.0 ** 3)))
    free_gb = float("{:.2f}".format(obj_Disk.free / (1024.0 ** 3)))
    free_percent = float("{:.2f}".format(obj_Disk.percent))
    
    drive_info = f"Drive: {drive_label}\nTotal: {total_gb} GB\nUsed: {used_gb} GB\nFree: {free_gb} GB\nFree %: {free_percent}"

    drive_label = tk.Label(show_breakdown_window, text=drive_info, bg="#93a8f5", fg="#000000",font=("Helvetica", 10, "bold"))
    drive_label.grid(row=0,column=0,columnspan=2,padx=20,pady=10)


def drive_specific(drive):
    
    window = tk.Toplevel(root)
    window.title(f"Drive {drive[:2]}")
    # window.geometry("600x400")
    window.config(bg="#93a8f5")
    show_breakdown_btn = tk.Button(window, text="Usage Breakdown", bg="#f0f0f0", fg="#000000",font=("Helvetica", 10, "bold"),width=40,command=partial(show_breakdown,drive,window))
    show_breakdown_btn.grid(row=0,column=1,columnspan=2,padx=20,pady=10)

root = tk.Tk()
root.title("Disk Space Manager")
root.geometry("600x400")
root.configure(bg="#93a8f5")
s = ttk.Style()
s.theme_use('winnative')

show_disk_usage()

root.mainloop()
