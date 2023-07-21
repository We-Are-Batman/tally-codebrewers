import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
import win32api
import psutil
import json
import os
import sys
from get_total_size_of_filetype import get_totalsize_of_filetype
from filterby_extension import filter_files_by_extension
from filter_by_filetype import filter_files_by_filetype
from get_large_files import get_large_files

extensions = {}

# Read from JSON file into a dictionary
with open('file_association.json') as json_file:
    extensions = json.load(json_file)

def validate_path(path):
    if os.path.isdir(path):
        error_label.config(text="")
        show_insights_page(path)
    else:
        error_label.config(text="Invalid path. Please enter a valid directory.")


def show_large_files_page(path,threshold=4*1024.0**2,extension="*"):

    def go_back():
        show_insights_page(path)
        frames["large_files"].destroy()

    frame = tk.Frame(root, bg="#93a8f5")

    frame1 = tk.Frame(frame, bg="#93a8f5")

    back_btn = tk.Button(frame1, text="Back", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=10, command=go_back)
    back_btn.pack(anchor='center',padx=20, pady=10)

    get_threshold_entry = ttk.Entry(frame1, width=20, font=("Helvetica", 10, "bold"))
    get_threshold_entry.pack(anchor='center',padx=20, pady=10,side="left")

    set_threshold_btn = tk.Button(frame1, text="Set Threshold", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=20,command=lambda: show_large_files_page(path,get_threshold_entry.get()))
    set_threshold_btn.pack(anchor='center',padx=20, pady=10,side="right")

    frame1.pack(anchor='center',padx=20, pady=10)

    s.configure("Treeview.Heading", foreground='blue', font=("Helvetica", 10, "bold"))

    tree = ttk.Treeview(frame,height=10)
    vsb = Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree["columns"]=("filename","size")
    tree["show"]="headings"

    tree.column("filename",minwidth=100, anchor="w")
    tree.column("size",minwidth=100, anchor=tk.CENTER)
    tree.heading("filename", text="File Name",anchor=tk.CENTER)
    tree.heading("size", text="Size",anchor=tk.CENTER)
    tree.pack(side='left',padx=20, pady=10)

    vsb.pack(side="right", fill="y")
    threshold = float(threshold)
    files = get_large_files(path, threshold, extension)

    for size,file,_ in files:
        size = float("{:.2f}".format(size / (1024.0)))
        size = f"{size} KB"
        tree.insert("", tk.END, values=(file,size))
    
    if len(files) == 0:
        tree.insert("", tk.END, values=("No files found",""))
    
    for f in frames.values():
        f.pack_forget()

    frame.pack(anchor='center',padx=20, pady=10)

    frames["large_files"] = frame
    frames["large_files_1"] = frame1

def show_filter_by_filetype_page(path,filetype,files_dict):

    def go_back():
        show_insights_page(path)
        frames["filter_by_filetype"].destroy()
    

    frame = tk.Frame(root, bg="#93a8f5")

    frame1 = tk.Frame(frame, bg="#93a8f5")

    back_btn = tk.Button(frame1, text="Back", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=10, command=go_back)
    back_btn.pack(anchor='center',padx=20, pady=10)

    #add a combo box to select the file type and add a btn to its right
    select_filetype_combo = ttk.Combobox(frame1, width=20, font=("Helvetica", 10, "bold"))
    select_filetype_combo['values'] = list(files_dict.keys())

    select_filetype_combo.pack(anchor='center',padx=20, pady=10,side="left")


    filter_by_filetype_btn = tk.Button(frame1, text="Search By Type", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=20,command=lambda: show_filter_by_filetype_page(path,select_filetype_combo.get(),files_dict))
    filter_by_filetype_btn.pack(anchor='center',padx=20, pady=10,side="right")

    frame1.pack(anchor='center',padx=20, pady=10)

    s.configure("Treeview.Heading", foreground='blue', font=("Helvetica", 10, "bold"))
    tree = ttk.Treeview(frame,height=10)
    vsb = Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree["columns"]=("filename","size")
    tree["show"]="headings"
    
    tree.column("filename",minwidth=100, anchor="w")
    tree.column("size",minwidth=100, anchor=tk.CENTER)
    tree.heading("filename", text="File Name",anchor=tk.CENTER)
    tree.heading("size", text="Size",anchor=tk.CENTER)
    tree.pack(side='left',padx=20, pady=10)
    vsb.pack(side="right", fill="y")
    files = filter_files_by_filetype(path, filetype)

    

    for file,size in files:
        size = float("{:.2f}".format(size / (1024.0)))
        size = f"{size} KB"
        tree.insert("", tk.END, values=(file,size))

    if len(files) == 0:
        tree.insert("", tk.END, values=("No files found",""))

    for f in frames.values():
        f.pack_forget()    
    
    frame.pack(anchor='center',padx=20, pady=10)
    frames["filter_by_filetype"] = frame
    frames["filter_by_filter_by_filetype_1"] = frame1

def show_filter_by_extension_page(path,ext):


    def go_back():
        show_insights_page(path)
        frames["filter_by_extension"].destroy()
    

    frame = tk.Frame(root, bg="#93a8f5")

    frame1 = tk.Frame(frame, bg="#93a8f5")

    back_btn = tk.Button(frame1, text="Back", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=10, command=go_back)
    back_btn.pack(anchor='center',padx=20, pady=10)
    get_extension_entry = ttk.Entry(frame1, width=20, font=("Helvetica", 10, "bold"))
    get_extension_entry.pack(anchor='center',padx=20, pady=10,side="left")

    filter_by_extension_btn = tk.Button(frame1, text="Search By Extension", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=20,command=lambda: show_filter_by_extension_page(path,get_extension_entry.get()))
    filter_by_extension_btn.pack(anchor='center',padx=20, pady=10,side="right")

    

   
    frame1.pack(anchor='center',padx=20, pady=10)
    s.configure("Treeview.Heading", foreground='blue', font=("Helvetica", 10, "bold"))
    tree = ttk.Treeview(frame,height=10)
    vsb = Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree["columns"]=("filename","size")
    tree["show"]="headings"
    
    tree.column("filename",minwidth=100, anchor="w")
    tree.column("size",minwidth=100, anchor=tk.CENTER)
    tree.heading("filename", text="File Name",anchor=tk.CENTER)
    tree.heading("size", text="Size",anchor=tk.CENTER)
    tree.pack(side='left',padx=20, pady=10)
    vsb.pack(side="right", fill="y")
    files = filter_files_by_extension(path,ext)

    

    for file,size in files:
        size = float("{:.2f}".format(size / (1024.0)))
        size = f"{size} KB"
        tree.insert("", tk.END, values=(file,size))

    if len(files) == 0:
        tree.insert("", tk.END, values=("No files found",""))

    for f in frames.values():
        (f)
        f.pack_forget()    
    
    frame.pack(anchor='center',padx=20, pady=10)
    frames["filter_by_extension"] = frame
    frames["filter_by_extension_1"] = frame1


def show_disk_usage(path,frame,row_count):
    drive_name = path[:2]
    # print(path)
    obj_Disk = psutil.disk_usage(path)
    total_gb = float("{:.2f}".format(obj_Disk.total / (1024.0 ** 3)))
    used_gb = float("{:.2f}".format(obj_Disk.used / (1024.0 ** 3)))
    free_gb = float("{:.2f}".format(obj_Disk.free / (1024.0 ** 3)))
    free_percent = float("{:.2f}".format(obj_Disk.percent))
    
    path_info = f"Path: {path}\n Total: {total_gb} GB\nUsed: {used_gb} GB\nFree: {free_gb} GB\nFree %: {free_percent}"

    # print(path_info)
    
    # Add a disabled button to show disk usage
    drive_button = tk.Button(frame, text=path_info, bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=40)
    drive_button.pack(anchor='center',padx=20, pady=10)


def show_insights_page(path):

    def go_back():
        show_homepage()
        frames["insights"].destroy()

    insights_frame = tk.Frame(root, bg="#93a8f5")
    

    files_dict,totalsize = get_totalsize_of_filetype(path)
    totalsize = float("{:.2f}".format(totalsize / (1024.0)))

    row_count = 0

    back_btn = tk.Button(insights_frame, text="Back", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=10, command=go_back)
    back_btn.pack(anchor='center',padx=20, pady=10)
    row_count += 1

    #label to show the path
    path_label = tk.Label(insights_frame, text=f"Path: {path}", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"),  relief="solid", borderwidth=1)
    path_label.pack(anchor='center',padx=20, pady=10)
    row_count += 1

    #solid border label
    totalsize_label = tk.Label(insights_frame, text=f"Total Disk Usage : {totalsize} KB", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=40, relief="solid", borderwidth=1)
    totalsize_label.pack(anchor='center',padx=20, pady=10)
    row_count += 1


    s.configure("Treeview.Heading", foreground='blue', font=("Helvetica", 10, "bold"))
    tree = ttk.Treeview(insights_frame,height=5)
    tree["columns"]=("filetype","size","percentage")
    tree["show"]="headings"

    tree.column("filetype", width=100,minwidth=100, anchor=tk.CENTER)
    tree.column("size",width=100,minwidth=100, anchor=tk.CENTER)
    tree.column("percentage", width=100,minwidth=100, anchor=tk.CENTER)
    tree.heading("filetype", text="File Type",anchor=tk.CENTER)
    tree.heading("size", text="Size",anchor=tk.CENTER)
    tree.heading("percentage", text="Percentage",anchor=tk.CENTER)
    tree.pack(anchor='center',padx=20, pady=10)

    for file_type, size in files_dict.items():
        tot = float("{:.2f}".format(size / (1024.0)))
        percentage = float("{:.2f}".format((tot/totalsize)*100))
        tot = f"{tot} KB"
        percentage = f"{percentage} %"
        tree.insert("", tk.END, values=(file_type,tot,percentage))

    detect_duplicate_btn = tk.Button(insights_frame, text="Detect Duplicates", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=40)
    detect_duplicate_btn.pack(anchor='center',padx=20, pady=10)

    id_large_files_btn = tk.Button(insights_frame, text="Identify Large Files", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=40,command=lambda: show_large_files_page(path))
    id_large_files_btn.pack(anchor='center',padx=20, pady=10)

    frame1 = tk.Frame(insights_frame, bg="#93a8f5")
    #add a combo box to select the file type and add a btn to its right
    select_filetype_combo = ttk.Combobox(frame1, width=20, font=("Helvetica", 10, "bold"))
    select_filetype_combo['values'] = list(files_dict.keys())
    select_filetype_combo.current(0)

    select_filetype_combo.pack(anchor='center',padx=20, pady=10,side="left")


    filter_by_filetype_btn = tk.Button(frame1, text="Search By Type", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=20,command=lambda: show_filter_by_filetype_page(path,select_filetype_combo.get(),files_dict))
    filter_by_filetype_btn.pack(anchor='center',padx=20, pady=10,side="right")

    frame1.pack(anchor='center',padx=20, pady=10)

    frame2 = tk.Frame(insights_frame, bg="#93a8f5")

    #add a combo box to select the file type and add a btn to its right
    get_extension_entry = ttk.Entry(frame2, width=20, font=("Helvetica", 10, "bold"))
    get_extension_entry.pack(anchor='center',padx=20, pady=10,side="left")

    filter_by_extension_btn = tk.Button(frame2, text="Search By Extension", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=20,command=lambda: show_filter_by_extension_page(path,get_extension_entry.get()))
    filter_by_extension_btn.pack(anchor='center',padx=20, pady=10,side="right")

    frame2.pack(anchor='center',padx=20, pady=10)

    for frame in frames.values():
        frame.pack_forget()

    insights_frame.pack(anchor='center',padx=20, pady=10)
    frames["insights"] = insights_frame
    frames["insights_1"] = frame1
    frames["insights_2"] = frame2

    

def show_homepage():
    for frame in frames.values():
        frame.pack_forget()
    
    frames["home"].pack(anchor='center',padx=20, pady=10)

if __name__ == "__main__":

    path=""

    if len(sys.argv) == 2:
        path = sys.argv[1]
        
    root = tk.Tk()
    root.title("Disk Space Manager")
    # root.geometry("600x400")  # Set the window size

    root.configure(bg="#93a8f5")
    s = ttk.Style()
    s.theme_use('winnative')

    #store all frames in a dictionary
    frames = {}

    #create home frame
    home_frame = tk.Frame(root, bg="#93a8f5")
    row_count = 0
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    for drive in drives:
        show_disk_usage(drive, home_frame,row_count)
        row_count += 1

    input_path_label = tk.Label(home_frame, text="Enter Path", bg="#93a8f5", font=("Helvetica", 10, "bold"), width=40)
    input_path_label.pack(anchor='center',padx=20, pady=10)
    row_count += 1

    input_path_text = tk.StringVar(value=path)
    input_path_entry = tk.Entry(home_frame, textvariable=input_path_text, width=50)
    input_path_entry.pack(anchor='center',padx=20, pady=10)
    row_count += 1

    get_insights_btn = tk.Button(home_frame, text="Get Insights", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=40, command=lambda: validate_path(input_path_text.get()))
    get_insights_btn.pack(anchor='center',padx=20, pady=10)
    row_count += 1

    error_label = tk.Label(home_frame, text="", fg="red", bg="#93a8f5")
    error_label.pack(anchor='center',padx=20, pady=10)
    row_count += 1

    frames["home"] = home_frame

    show_homepage()


    root.mainloop()
