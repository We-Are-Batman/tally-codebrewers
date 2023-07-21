import concurrent.futures
import os
import json
from get_extension import identify_file_extension

extensions = {}

# Read from JSON file into a dictionary
with open('file_association.json') as json_file:
    extensions = json.load(json_file)


def filter_files_by_filetype(root_path, filetype):
    found_files = []

    def filter_by_filetype(dir_path, filetype):
        file_list = []
        for root, _, files in os.walk(dir_path):
            for filename in files:
                # print(filename)
                file_path = os.path.join(root, filename)
                file_stats = os.stat(file_path)
                file_extension = identify_file_extension(file_path)
                if len(file_extension) < 1:
                    continue
                if file_extension not in extensions:
                    actual_type = "documents"
                else:
                    actual_type = extensions[file_extension]

                # print(actual_type,fi)
                if actual_type == filetype:
                    # print("yes")
                    size = file_stats.st_size
                    file_list.append((filename, size))

        return file_list

    def process_directory(dir_path):
        file_list = filter_by_filetype(dir_path, filetype)
        found_files.extend(file_list)

    # Get a list of all directories in the root path
    directories = []
    for d in os.listdir(root_path):
        if os.path.isdir(os.path.join(root_path, d)):
            directories.append(os.path.join(root_path, d))
        elif os.path.isfile(os.path.join(root_path, d)):
            try:
                # print(d)
                file_path = os.path.join(root_path, d)
                file_stats = os.stat(file_path)
                file_extension = identify_file_extension(file_path)
                if len(file_extension) < 1:
                    continue
                if file_extension not in extensions:
                    actual_type = "documents"
                else:
                    actual_type = extensions[file_extension]

                if actual_type == filetype:
                    # print("yes")
                    size = file_stats.st_size
                    found_files.append((d, size))
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
        
    return found_files
