import os
import concurrent.futures
import json


extensions = {}

# read from  json file into dictionary

with open('file_association.json') as json_file:
    extensions = json.load(json_file)


def get_totalsize_of_filetype(root_path):
    found_files = {}

    def find_files(directory):
        file_dict = {}
        for root, _, files in os.walk(directory):
            for filename in files:
                try:
                    # print(filename)
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

                    if file_dict.get(actual_type) == None:
                        file_dict[actual_type] = 0

                    file_dict[actual_type] = file_dict[actual_type] + \
                        file_stats.st_size

                except:
                    pass
        return file_dict

    def process_directory(dir_path):
        file_dict = find_files(dir_path)
        found_files.update(file_dict)

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


if __name__ == "__main__":
    # Replace with the drive letter you want to search
    drive_path = r"C:\Users\adnan\OneDrive\Pictures\Screenshots"
    # Add more extensions if needed

    found_files = get_totalsize_of_filetype(drive_path)
    print(f"Found {len(found_files)} file types in path {drive_path}:")
    for extension, size in found_files.items():
        tot = float("{:.2f}".format(size / (1024.0)))
        print(f"for extension {extension} size is {tot} KB")
