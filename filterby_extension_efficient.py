import tkinter as tk
from tkinter import ttk
import concurrent.futures
import os
import json

extensions = {}

path = "C:\\Users\\adnan\\OneDrive\\Pictures\\Camera Roll"
filetype = "video"
ext = ".jpg"

# Read from JSON file into a dictionary
with open('file_association.json') as json_file:
    extensions = json.load(json_file)


def filter_files_by_extension(root_path, ext):
    found_files = []

    def filter_by_ext(dir_path, ext):
        file_list = []
        for _, _, files in os.walk(dir_path):
            for filename in files:
                split_tup = os.path.splitext(filename)
                file_extension = split_tup[1]
                if len(file_extension) < 1:
                    continue
                if file_extension == ext:
                    print(filename)
                    file_list.append(filename)

        return file_list

    def process_directory(dir_path):
        file_list = filter_by_ext(dir_path, ext)
        found_files.extend(file_list)

    # Get a list of all directories in the root path
    directories = [os.path.join(root_path, d) for d in os.listdir(
        root_path) if os.path.isdir(os.path.join(root_path, d))]

    # Create a ThreadPoolExecutor with a number of threads (use as many as the number of CPU cores)
    num_threads = min(len(directories), os.cpu_count())
    if num_threads == 0:
        process_directory(root_path)
        return found_files
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_directory = {executor.submit(
                process_directory, directory): directory for directory in directories}

            # Wait for all threads to finish
            for future in concurrent.futures.as_completed(future_to_directory):
                directory = future_to_directory[future]
                try:
                    future.result()  # Get the result of the thread, but we don't use it here
                except Exception as e:
                    print(
                        f"An error occurred while searching in {directory}: {e}")
        return found_files


# Call the function with the desired path and filetype
files = filter_files_by_extension(path, ext)

for file in files:
    print(file)