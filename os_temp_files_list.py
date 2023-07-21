import tempfile
import concurrent.futures
import os

def get_file_category(file_path):
    file_name = os.path.basename(file_path).lower()

    # Installation files pattern
    installation_patterns = ['setup', 'install', 'msi', 'exe', 'dmg']

    # Log files pattern
    log_patterns = ['log', 'log-', '.log']

    # Backup files pattern
    backup_patterns = ['backup', 'bak', '.bak']

    # Cached files pattern
    cached_patterns = ['cache', 'temp', 'tmp', '.temp', '.tmp']

    for pattern_list, category in [
        (installation_patterns, 'Installation'),
        (log_patterns, 'Log'),
        (backup_patterns, 'Backup'),
        (cached_patterns, 'Cached')
    ]:
        for pattern in pattern_list:
            if pattern in file_name:
                return category

    return 'Other'

def get_temp_files_info():
    temp_dir = tempfile.gettempdir()
    temp_files_info = []
    total_size = 0

    def find_files(directory):
        lst = []
        size = 0
        for root, _, files in os.walk(directory):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    file_stats = os.stat(file_path)
                    file_size = file_stats.st_size
                    file_category = get_file_category(file_path)
                    lst.append(( file, file_category ,file_size))
                    size += file_size
                except:
                    pass

        return lst,size
    
    def process_directory(dir_path):
        nonlocal total_size
        lst,size = find_files(dir_path)
        temp_files_info.extend(lst)
        total_size += size

    directories = []
    for d in os.listdir(temp_dir):
        if os.path.isdir(os.path.join(temp_dir, d)):
            directories.append(os.path.join(temp_dir, d))
        elif os.path.isfile(os.path.join(temp_dir, d)):
            try:
                file_path = os.path.join(temp_dir, d)
                file_stats = os.stat(file_path)
                file_size = file_stats.st_size
                file_category = get_file_category(file_path)
                temp_files_info.append(( d, file_category ,file_size))
                total_size += file_size
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

    return temp_files_info, total_size

# if __name__ == "__main__":
#     files,size = get_temp_files_info()
#     for file_info in files:
#         print(file_info)
