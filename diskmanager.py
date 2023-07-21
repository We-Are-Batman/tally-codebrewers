import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
from tkinter import filedialog
import win32api
import psutil
import json
import os
import sys
from get_total_size_of_filetype import get_totalsize_of_filetype
from filterby_extension import filter_files_by_extension
from filter_by_filetype import filter_files_by_filetype
from get_large_files import get_large_files
from duplicate_files import *
from preview_file import preview_file
from os_temp_files_size import get_temp_files_info

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


def show_duplicate_files_page(path):

    def go_back():
        show_insights_page(path)
        frames["duplicate_files"].destroy()

    def preview_btn_click():
        selected_item = tree.selection()
        if selected_item:
            selected_row = tree.item(selected_item)
            selected_path = selected_row['values'][0]  # Assuming the path is in the first column 'fpath'
            preview_file(selected_path)
    
    ind =0

    def insert_in_tree():
        nonlocal ind
        nonlocal duplicate_files_len
        page_number_var.set(f"Page {ind+1} of {duplicate_files_len}")
        tree.delete(*tree.get_children())
        if ind == 0:
            previous_btn.configure(state="disabled")
        else:
            previous_btn.configure(state="normal")
        if ind == duplicate_files_len-1:
            next_btn.configure(state="disabled")
        else:
            next_btn.configure(state="normal")
        for fpath,size,name in duplicate_files[ind]:
            size = float("{:.2f}".format(size / (1024.0)))
            if size < 1:
                size = 1
            size = int(size)
            size = f"{size} KB"
            tree.insert("", tk.END, values=(fpath,size,name))

    def next():
        nonlocal ind
        ind += 1
        insert_in_tree()
    
    def previous():
        nonlocal ind
        ind -= 1
        insert_in_tree()

    frame = tk.Frame(root, bg="#93a8f5")

    frame1 = tk.Frame(frame, bg="#93a8f5")

    title_label = tk.Label(frame1, text="Duplicate Files", bg="#93a8f5", font=("Helvetica", 10, "bold"), width=40)
    title_label.pack(anchor='center',padx=20, pady=10)

    back_btn = tk.Button(frame1, text="Back", bg="#f0f0f0", fg="#000000",font=("Helvetica", 10, "bold"),width=20,command=go_back)
    back_btn.pack(anchor='center',padx=20, pady=10)

    page_number_var = tk.StringVar(value="Page 1 of 1")
    page_number_label = tk.Label(frame1, textvariable=page_number_var, bg="#93a8f5", font=("Helvetica", 10, "bold"), width=40)
    page_number_label.pack(anchor='center',padx=20, pady=10)

    help_label = tk.Label(frame1, text="Use Ctrl + Left Click to select multiple files", bg="#93a8f5", font=("Helvetica", 10))
    help_label.pack(anchor='w',padx=20, pady=10)

    s.configure("Treeview.Heading", foreground='blue', font=("Helvetica", 10, "bold"))

    tree = ttk.Treeview(frame1,height=10)
    vsb = Scrollbar(frame1, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree["columns"]=("fpath","size","fname")
    tree["show"]="headings"

    tree.column("fpath",minwidth=100,width=300, anchor="w")
    tree.column("size",minwidth=100, anchor=tk.CENTER)
    tree.column("fname",minwidth=100, anchor=tk.CENTER)
    tree.heading("fpath", text="Path",anchor=tk.CENTER)
    tree.heading("size", text="Size",anchor=tk.CENTER)
    tree.heading("fname", text="File Name",anchor=tk.CENTER)

    tree.pack(side='left',padx=20, pady=10)

    vsb.pack(side="right", fill="y")

    
    frame1.pack(anchor='center',padx=20, pady=10)

    frame2 = tk.Frame(frame, bg="#93a8f5")

    previous_btn = tk.Button(frame2, text="Previous", bg="#f0f0f0", fg="#000000",font=("Helvetica", 10, "bold"),width=20,command=previous)
    previous_btn.pack(anchor='center',padx=20, pady=10,side="left")
    previous_btn.configure(state="disabled")

    next_btn = tk.Button(frame2, text="Next", bg="#f0f0f0", fg="#000000",font=("Helvetica", 10, "bold"),width=20,command=next)
    next_btn.pack(anchor='center',padx=20, pady=10,side="right")
    next_btn.configure(state="disabled")

    frame2.pack(anchor='center',padx=20, pady=10)

    frame3 = tk.Frame(frame, bg="#93a8f5")

    preview_btn = tk.Button(frame3, text="Preview", bg="#f0f0f0", fg="#0000ff",font=("Helvetica", 10, "bold"),width=40,command=lambda: preview_btn_click())
    preview_btn.pack(anchor='center',padx=20, pady=10)

    delete_auto_btn = tk.Button(frame3, text="Delete Automatically", bg="#f0f0f0", fg="#ff0000",font=("Helvetica", 10, "bold"),width=40)
    delete_auto_btn.pack(anchor='center',padx=20, pady=10)

    delete_manually_btn = tk.Button(frame3, text="Delete Manually", bg="#f0f0f0", fg="#ff0000",font=("Helvetica", 10, "bold"),width=40)
    delete_manually_btn.pack(anchor='center',padx=20, pady=10)

    frame3.pack(anchor='center',padx=20, pady=10)

    duplicate_files = find_duplicate_files(path)

    #convert this to a list of lists
    duplicate_files = list(duplicate_files.values())

    duplicate_files_len = len(duplicate_files)

    

    if duplicate_files_len == 0:
        tree.insert("", tk.END, values=("No files found","",""))
    else:
        insert_in_tree()


    for f in frames.values():
        f.pack_forget()
    
    frame.pack(anchor='center',padx=20, pady=10)

    frames["duplicate_files"] = frame
    frames["duplicate_files_1"] = frame1
    frames["duplicate_files_2"] = frame2
    frames["duplicate_files_3"] = frame3

    
        



def show_large_files_page(path,threshold=4*1024.0,extension="*"):

    def go_back():
        show_insights_page(path)
        frames["large_files"].destroy()
    
    def preview_btn_click():
        selected_item = tree.selection()
        if selected_item:
            selected_row = tree.item(selected_item)
            selected_path = selected_row['values'][0]  # Assuming the path is in the first column 'fpath'
            selected_path = os.path.join(path,selected_path)
            preview_file(selected_path)

    frame = tk.Frame(root, bg="#93a8f5")

    frame1 = tk.Frame(frame, bg="#93a8f5")

    back_btn = tk.Button(frame1, text="Back", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=10, command=go_back)
    back_btn.pack(anchor='center',padx=20, pady=10)

    get_threshold_entry = ttk.Entry(frame1, width=20, font=("Helvetica", 10, "bold"))
    get_threshold_entry.pack(anchor='center',padx=20, pady=10,side="left")

    set_threshold_btn = tk.Button(frame1, text="Set Threshold in KB", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=20,command=lambda: show_large_files_page(path,get_threshold_entry.get()))
    set_threshold_btn.pack(anchor='center',padx=20, pady=10,side="right")

    frame1.pack(anchor='center',padx=20, pady=10)

    s.configure("Treeview.Heading", foreground='blue', font=("Helvetica", 10, "bold"))

    frame2= tk.Frame(frame, bg="#93a8f5")

    tree = ttk.Treeview(frame2,height=10)
    vsb = Scrollbar(frame2, orient="vertical", command=tree.yview)
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
    threshold = threshold * 1024.0

    frame2.pack(anchor='center',padx=20, pady=10)

    files = get_large_files(path, threshold, extension)

    frame3 = tk.Frame(frame, bg="#93a8f5")

    preview_btn = tk.Button(frame3, text="Preview", bg="#f0f0f0", fg="#0000ff",font=("Helvetica", 10, "bold"),width=40,command=lambda: preview_btn_click())
    preview_btn.pack(anchor='center',padx=20, pady=10)


    delete_manually_btn = tk.Button(frame3, text="Delete", bg="#f0f0f0", fg="#ff0000",font=("Helvetica", 10, "bold"),width=40)
    delete_manually_btn.pack(anchor='center',padx=20, pady=10)

    frame3.pack(anchor='center',padx=20, pady=10)


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
    
    def preview_btn_click():
        selected_item = tree.selection()
        if selected_item:
            selected_row = tree.item(selected_item)
            selected_path = selected_row['values'][0]  # Assuming the path is in the first column 'fpath'
            selected_path = os.path.join(path,selected_path)
            preview_file(selected_path)
    

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

    frame2= tk.Frame(frame, bg="#93a8f5")

    tree = ttk.Treeview(frame2,height=10)
    vsb = Scrollbar(frame2, orient="vertical", command=tree.yview)
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

    frame2.pack(anchor='center',padx=20, pady=10)

    frame3 = tk.Frame(frame, bg="#93a8f5")

    preview_btn = tk.Button(frame3, text="Preview", bg="#f0f0f0", fg="#0000ff",font=("Helvetica", 10, "bold"),width=40,command=lambda: preview_btn_click())
    preview_btn.pack(anchor='center',padx=20, pady=10)


    delete_manually_btn = tk.Button(frame3, text="Delete", bg="#f0f0f0", fg="#ff0000",font=("Helvetica", 10, "bold"),width=40)
    delete_manually_btn.pack(anchor='center',padx=20, pady=10)

    frame3.pack(anchor='center',padx=20, pady=10)

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
    frames["filter_by_filter_by_filetype_2"] = frame2
    frames["filter_by_filter_by_filetype_3"] = frame3

def show_filter_by_extension_page(path,ext):


    def go_back():
        show_insights_page(path)
        frames["filter_by_extension"].destroy()
    
    def preview_btn_click():
        selected_item = tree.selection()
        if selected_item:
            selected_row = tree.item(selected_item)
            selected_path = selected_row['values'][0]  # Assuming the path is in the first column 'fpath'
            selected_path = os.path.join(path,selected_path)
            preview_file(selected_path)
    

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

    frame2= tk.Frame(frame, bg="#93a8f5")

    tree = ttk.Treeview(frame2,height=10)
    vsb = Scrollbar(frame2, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree["columns"]=("filename","size")
    tree["show"]="headings"
    
    tree.column("filename",minwidth=100, anchor="w")
    tree.column("size",minwidth=100, anchor=tk.CENTER)
    tree.heading("filename", text="File Name",anchor=tk.CENTER)
    tree.heading("size", text="Size",anchor=tk.CENTER)
    tree.pack(side='left',padx=20, pady=10)
    vsb.pack(side="right", fill="y")

    frame2.pack(anchor='center',padx=20, pady=10)

    files = filter_files_by_extension(path,ext)

    frame3 = tk.Frame(frame, bg="#93a8f5")

    preview_btn = tk.Button(frame3, text="Preview", bg="#f0f0f0", fg="#0000ff",font=("Helvetica", 10, "bold"),width=40,command=lambda: preview_btn_click())
    preview_btn.pack(anchor='center',padx=20, pady=10)


    delete_manually_btn = tk.Button(frame3, text="Delete", bg="#f0f0f0", fg="#ff0000",font=("Helvetica", 10, "bold"),width=40)
    delete_manually_btn.pack(anchor='center',padx=20, pady=10)

    frame3.pack(anchor='center',padx=20, pady=10)

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
    frames["filter_by_extension_2"] = frame2
    frames["filter_by_extension_3"] = frame3


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

    detect_duplicate_btn = tk.Button(insights_frame, text="Detect Duplicates", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=40,command=lambda: show_duplicate_files_page(path))
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

def browse_directory():
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            input_path_text.set(selected_dir)

if __name__ == "__main__":

    path=""

    if len(sys.argv) == 2:
        path = sys.argv[1]

    print(path)
    

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
    
    os_temp_var = tk.StringVar(value="")

    def process_temp_files():
        _, total_size = get_temp_files_info()
        total_size = float("{:.2f}".format(total_size / (1024.0**3)))
        total_size = f"{total_size} GB"
        os_temp_var.set(f"Clear Temp Files\nTotal Size : {total_size}")

    
    process_temp_files()

    os_temp_label = tk.Button(home_frame, textvariable=os_temp_var, bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=40)
    os_temp_label.pack(anchor='center',padx=20, pady=10)

    input_path_label = tk.Label(home_frame, text="Enter Path", bg="#93a8f5", font=("Helvetica", 10, "bold"), width=40)
    input_path_label.pack(anchor='center',padx=20, pady=10)
    row_count += 1

    input_path_text = tk.StringVar(value=path)
    input_path_entry = tk.Entry(home_frame, textvariable=input_path_text, width=50)
    input_path_entry.pack(anchor='center',padx=20, pady=10)
    row_count += 1

    browse_btn = tk.Button(home_frame, text="Browse", bg="#f0f0f0", fg="#000000", font=("Helvetica", 10, "bold"), width=40, command=browse_directory)
    browse_btn.pack(anchor='center', padx=20, pady=10)
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
