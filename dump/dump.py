import tkinter as tk
from tkinter import ttk
from functools import partial
import win32api
import psutil
import json
import os

extensions = {}

#read from  json file into dictionary
with open('file_association.json') as json_file:
    extensions = json.load(json_file)


# def filter_by_filetype(dir_path,filetype):
#     file_list = []
#     for root, _, files in os.walk(dir_path):
#         for filename in files:
#             file_path = os.path.join(root, filename)
#             split_tup = os.path.splitext(filename)
#             file_extension = split_tup[1]
#             if len(file_extension)<1:
#                 continue
#             if file_extension not in extensions:
#                 actual_type = "documents"
#             else:
#                 actual_type = extensions[file_extension]

#             if actual_type == filetype:
#                 file_list.append(file_path)
        
#     # return file_list
#     for file in file_list:
#         print(file)

# ### function to return file type with total size
# def categorize_by_filetype(dir_path):
#     # file_list = []
#     file_dict = {}

#     for root, _, files in os.walk(dir_path):
#         # print(root)
#         for filename in files:
#             file_path = os.path.join(root, filename)
#             try: 
#                 file_stats = os.stat(file_path)
#             except:
#                 continue
#             split_tup = os.path.splitext(filename)
#             file_extension = split_tup[1]
#             if len(file_extension)<1:
#                 continue
#             if file_extension not in extensions:
#                 actual_type = "documents"
#             else:
#                 actual_type = extensions[file_extension]

#             # print(filename,file_extension)
#             if file_dict.get(actual_type)==None:
#                 file_dict[actual_type] = 0

#             file_dict[actual_type] = file_dict[actual_type] +  file_stats.st_size


#     # return file_dict
#     for extension,size in file_dict.items():
#         tot = float("{:.2f}".format(size / (1024.0)))
#         print(f"for extension {extension} size is {tot} KB")

def show_disk_usage(path):
    # drives = win32api.GetLogicalDriveStrings()
    # drives = drives.split('\000')[:-1]
    
    # for drive in drives:
        # drive_label = drive[:2]
        obj_Disk = psutil.disk_usage(path)
        total_gb = float("{:.2f}".format(obj_Disk.total / (1024.0 ** 3)))
        used_gb = float("{:.2f}".format(obj_Disk.used / (1024.0 ** 3)))
        free_gb = float("{:.2f}".format(obj_Disk.free / (1024.0 ** 3)))
        free_percent = float("{:.2f}".format(obj_Disk.percent))
        
        drive_info = f"Total: {total_gb} GB\nUsed: {used_gb} GB\nFree: {free_gb} GB\nFree %: {free_percent}"
        
        #display pie chart here 

# def show_breakdown(drive,root):
#     show_breakdown_window = tk.Toplevel(root)
#     show_breakdown_window.title(f"Drive {drive} Usage Breakdown")
#     show_breakdown_window.geometry("600x400")
#     show_breakdown_window.config(bg="#93a8f5")
    

#     drive_label = tk.Label(show_breakdown_window, text=drive_info, bg="#93a8f5", fg="#000000",font=("Helvetica", 10, "bold"))
#     drive_label.grid(row=0,column=0,columnspan=2,padx=20,pady=10)


# def drive_specific(drive):
#     path = "C:\\Users\\adnan\\OneDrive\\Pictures\\Camera Roll"
#     window = tk.Toplevel(root)
#     window.title(f"Drive {drive[:2]}")
#     # window.geometry("600x400")
#     window.config(bg="#93a8f5")
#     show_breakdown_btn = tk.Button(window, text="Usage Breakdown", bg="#f0f0f0", fg="#000000",font=("Helvetica", 10, "bold"),width=40,command=partial(categorize_by_filetype,path))
#     show_breakdown_btn.grid(row=0,column=1,columnspan=2,padx=20,pady=10)

root = tk.Tk()
root.title("Disk Space Manager")
root.geometry("600x400")
root.configure(bg="#93a8f5")
s = ttk.Style()
s.theme_use('winnative')

drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000')[:-1]

for drive in drives:
      show_disk_usage(drive)
      

root.mainloop()
