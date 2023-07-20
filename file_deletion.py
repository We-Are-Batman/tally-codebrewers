import os
import threading
import shutil
def delete_files_thread(paths_list):
    for path in paths_list:
        try:
            if os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            print(f"Deleted: {path}")
        except Exception as e:
            print(f"Error deleting {path}: {e}")

def get_all_files_and_folders(directory):
    all_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            all_paths.append(file_path)
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            all_paths.append(folder_path)
    return all_paths

def delete_files_multithread(directory, num_threads=4):
    # Split the paths_to_delete list into smaller chunks for each thread
    paths_to_delete = [os.path.join(directory, file) for file in os.listdir(directory)]
    
    num_paths = len(paths_to_delete)
    if num_paths == 0:
        return
    num_threads = min(num_threads, num_paths)  # Adjust the number of threads if there are fewer paths than threads

    # Split the paths_to_delete list into smaller chunks for each thread
    chunk_size = num_paths // num_threads
    path_chunks = [paths_to_delete[i:i + chunk_size] for i in range(0, num_paths, chunk_size)]

    threads = []
    for chunk in path_chunks:
        thread = threading.Thread(target=delete_files_thread, args=(chunk,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    directory = r"C:\Users\kabir\OneDrive\Desktop\testfile"
    delete_files_multithread(directory)
