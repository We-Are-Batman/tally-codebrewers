import concurrent.futures
import os
import json

extensions = {}
# Read from JSON file into a dictionary
with open('file_association.json') as json_file:
    extensions = json.load(json_file)


def filter_files_by_extension(root_path, ext):
    if len(ext) < 1:
        return []
    found_files = []
    if ext[0] != '.':
        ext = '.' + ext
    def filter_by_ext(dir_path, ext):
        file_list = []
        for root, _, files in os.walk(dir_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_stats = os.stat(file_path)
                split_tup = os.path.splitext(filename)
                file_extension = split_tup[1]
                if len(file_extension) < 1:
                    continue
                if file_extension == ext:
                    size = file_stats.st_size
                    file_list.append((filename, size))

        return file_list

    def process_directory(dir_path):
        file_list = filter_by_ext(dir_path, ext)
        found_files.extend(file_list)

    # Get a list of all directories in the root path
    # directories = [os.path.join(root_path, d) for d in os.listdir(
    #     root_path) if os.path.isdir(os.path.join(root_path, d))]
    directories = []
    for d in os.listdir(root_path):
        if os.path.isdir(os.path.join(root_path, d)):
            directories.append(os.path.join(root_path, d))
        elif os.path.isfile(os.path.join(root_path, d)):
            try:
                # print(d)
                file_path = os.path.join(root_path, d)
                file_stats = os.stat(file_path)
                split_tup = os.path.splitext(d)
                file_extension = split_tup[1]
                if len(file_extension) < 1:
                    continue

                if file_extension == ext:
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