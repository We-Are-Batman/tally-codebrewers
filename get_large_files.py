import os
import concurrent.futures
import json


extensions = {}

# read from  json file into dictionary

with open('file_association.json') as json_file:
    extensions = json.load(json_file)


def get_large_files(root_path, thresold, extension):
    found_files = []

    def find_files(directory, lst, thresold, extension):
        for root, _, files in os.walk(directory):
            for filename in files:
                try:
                    file_path = os.path.join(root, filename)
                    file_stats = os.stat(file_path)
                    split_tup = os.path.splitext(filename)
                    file_extension = split_tup[1]
                    if len(file_extension) < 1:
                        continue
                    if file_extension not in extensions:
                        actual_type = "documents"
                    else:
                        actual_type = extensions[file_extension]

                    if extension != "*" and extension != actual_type:
                        continue

                    if file_stats.st_size < thresold:
                        continue
                    lst.append((file_stats.st_size, filename, file_path))
                except:
                    pass



    # Get a list of all directories in the root path
    directories = []
    for d in os.listdir(root_path):
        if os.path.isdir(os.path.join(root_path, d)):
            directories.append(os.path.join(root_path, d))
        elif os.path.isfile(os.path.join(root_path, d)):
            try:
                file_path = os.path.join(root_path, d)
                file_stats = os.stat(file_path)
                split_tup = os.path.splitext(d)
                file_extension = split_tup[1]
                if len(file_extension) < 1:
                    continue
                if file_extension not in extensions:
                    actual_type = "documents"
                else:
                    actual_type = extensions[file_extension]

                if extension != "*" and extension != actual_type:
                        continue
                if file_stats.st_size < thresold:
                    continue
                found_files.append((file_stats.st_size, d , file_path))
            except:
                    pass
            

    # Create a ThreadPoolExecutor with a number of threads (use as many as the number of CPU cores)
    num_threads = min(len(directories), os.cpu_count())
    if num_threads > 0:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_directory = {executor.submit(
                find_files, directory, found_files, thresold, extension): directory for directory in directories}

            # Wait for all threads to finish
            for future in concurrent.futures.as_completed(future_to_directory):
                directory = future_to_directory[future]
                try:
                    future.result()  # Get the result of the thread, but we don't use it here
                except Exception as e:
                    print(f"An error occurred while searching in {directory}: {e}")
        
        
    found_files.sort(key=lambda x: x[0], reverse=True)
    return found_files


# files = get_large_files("C:\\Users\\ACER\\Documents",200*1024,"*")
# for f in files:
#     print(f)