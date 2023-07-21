import os
import threading
import shutil
# from dotenv import dotenv

# load_dotenv()

# deleted_files_path=os.getenv(DELETION_PATH)
deleted_files_path=r"C:\Users\adnan\OneDrive\Desktop\recyclebin"


def ensure_folder_exists(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"Folder created: {folder_path}")
        except OSError as e:
            # Handle any errors that may occur during folder creation
            print(f"Error creating folder: {e}")

def delete_file(source_file_path):
    ensure_folder_exists(deleted_files_path);
    try:
    # Move the file from the source path to the destination path
        shutil.move(source_file_path, deleted_files_path)
        print(f"File moved successfully to {deleted_files_path}.")
    except FileNotFoundError:
        print("Source file not found.")
    except shutil.Error as e:
        print(f"An error occurred while moving the file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def delete_files_thread(paths_list):
    for path in paths_list:
        try:
            delete_file(path)
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

def delete_files_multithread(paths_to_delete, num_threads=4):
    # Split the paths_to_delete list into smaller chunks for each thread
    
    
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


import os
import shutil
import threading

def delete_bin_contents(folder_path=deleted_files_path):
    ensure_folder_exists(deleted_files_path)
    def delete_file_or_directory(path):
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            print(f"Error deleting {path}: {e}")

    try:
        # Get a list of all items in the folder (files and directories)
        items = [os.path.join(folder_path, item) for item in os.listdir(folder_path)]

        # Use multiple threads to delete files and directories in parallel
        num_threads = min(8, len(items))  # You can adjust the number of threads based on your system capacity
        chunk_size = len(items) // num_threads
        threads = []

        for i in range(0, len(items), chunk_size):
            chunk = items[i:i + chunk_size]
            thread = threading.Thread(target=lambda paths: [delete_file_or_directory(path) for path in paths], args=(chunk,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        print(f"All contents in {folder_path} deleted successfully.")
    except FileNotFoundError:
        print(f"Folder {folder_path} not found.")
    except Exception as e:
        print(f"An error occurred while deleting contents in {folder_path}: {e}")


if __name__ == "__main__":
    # directory = r"C:\Users\kabir\OneDrive\Desktop\testfile"
    # paths_to_delete = [os.path.join(directory, file) for file in os.listdir(directory)]
    # delete_files_multithread(paths_to_delete)
    delete_bin_contents()
