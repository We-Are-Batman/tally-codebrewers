import os
import concurrent.futures
import json
from get_extension import identify_file_extension


extensions = {}

# read from  json file into dictionary

with open('file_association.json') as json_file:
    extensions = json.load(json_file)




def get_totalsize_of_filetype(root_path):
    found_files = {}
    total_folder_size = 0

    def find_files(directory):
        file_dict = {}
        size = 0
        for root, _, files in os.walk(directory):
            for filename in files:
                try:
                    file_path = os.path.join(root, filename)
                    file_stats = os.stat(file_path)
                    # split_tup = os.path.splitext(filename,file_stats.st_size)
                    file_extension = identify_file_extension(file_path)
                    # print(filename,file_extension)
                    if len(file_extension) < 1:
                        continue
                    if file_extension not in extensions:
                        actual_type = "documents"
                    else:
                        actual_type = extensions[file_extension]

                    if file_dict.get(actual_type) == None:
                        file_dict[actual_type] = 0

                    file_dict[actual_type] = file_dict[actual_type] + file_stats.st_size
                    size = size + file_stats.st_size

                except:
                    pass
        return file_dict, size

    def process_directory(dir_path):
        nonlocal total_folder_size
        file_dict,folder_size = find_files(dir_path)
        found_files.update(file_dict)
        total_folder_size += folder_size


    directories = []
    for d in os.listdir(root_path):
        if os.path.isdir(os.path.join(root_path, d)):
            directories.append(os.path.join(root_path, d))
        elif os.path.isfile(os.path.join(root_path, d)):
            try:
                file_path = os.path.join(root_path, d)
                file_stats = os.stat(file_path)
                file_extension = identify_file_extension(file_path)
                # print(d,file_extension)
                if len(file_extension) < 1:
                    continue
                if file_extension not in extensions:
                    actual_type = "documents"
                else:
                    actual_type = extensions[file_extension]

                if found_files.get(actual_type) == None:
                    found_files[actual_type] = 0

                found_files[actual_type] = found_files[actual_type] + file_stats.st_size
                total_folder_size += file_stats.st_size
            except:
                pass
            

    # Create a ThreadPoolExecutor with a number of threads (use as many as the number of CPU cores)
    num_threads = min(len(directories), os.cpu_count())
    if num_threads > 0: 
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

    return found_files, total_folder_size


# files,size = get_totalsize_of_filetype("E://")
# for type,size in files.items():
#     print(type,size)
# print(size)