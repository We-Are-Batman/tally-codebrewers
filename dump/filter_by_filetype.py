import tkinter as tk
from tkinter import ttk
from functools import partial
import win32api
import psutil
import json
import os

extensions = {}

path = "C:\\Users\\adnan\\OneDrive\\Pictures\\Camera Roll"
ext = ".jpg"

filetype = "video"

#read from  json file into dictionary
with open('file_association.json') as json_file:
    extensions = json.load(json_file)


def filter_by_filetype(dir_path,filetype):
    file_list = []
    for _, _, files in os.walk(dir_path):
        for filename in files:
            split_tup = os.path.splitext(filename)
            file_extension = split_tup[1]
            if len(file_extension)<1:
                continue
            if file_extension not in extensions:
                actual_type = "documents"
            else:
                actual_type = extensions[file_extension]

            if actual_type == filetype:
                file_list.append(filename)
        
    # return file_list
    for file in file_list:
        print(file)

def filter_by_ext(dir_path,ext):
    file_list = []
    for _, _, files in os.walk(dir_path):
        for filename in files:
            split_tup = os.path.splitext(filename)
            file_extension = split_tup[1]
            if len(file_extension)<1:
                continue
            if file_extension == ext:
                file_list.append(filename)
        
    # return file_list
    for file in file_list:
        print(file)

filter_by_filetype(path,filetype)
print("--------------------------------------------------")
filter_by_ext(path,ext)