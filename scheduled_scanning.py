import os
import schedule
import time
import hashlib
from duplicate_files import find_duplicate_files
import wmi 
import psutil
import shutil
import datetime
from add_list_to_zip import create_zip
from dotenv import load_dotenv

load_dotenv()
log_files_path=os.getenv("LOG_FILE_PATH")
folder_path=os.getenv("SCANNING_FOLDER_PATH")
print(log_files_path)
def send_old_files_to_archive(file_paths, archive_location, days_threshold):
    try:
        now = datetime.now()

        # Filter files older than the specified threshold (days_threshold)
        old_files = [file_path for file_path in file_paths if (now - datetime.fromtimestamp(os.path.getmtime(file_path))).days > days_threshold]

        if not old_files:
            print("No files older than the threshold found.")
            return

        # Create a temporary folder to store the files before zipping
        temp_folder = os.path.join(archive_location, "temp")
        os.makedirs(temp_folder, exist_ok=True)

        # Move the old files to the temporary folder
        for file_path in old_files:
            shutil.move(file_path, temp_folder)

        # Zip the files in the temporary folder
        archive_name = os.path.join(archive_location, f"archive_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip")
        create_zip(old_files, archive_name)

        # Remove the temporary folder after zipping
        shutil.rmtree(temp_folder)

        print("Old files successfully archived.")
    except Exception as e:
        print(f"Error: {e}")



def get_available_drives():
    drives = []
    for drive in range(65, 91):
        drive_letter = chr(drive) + ":\\"
        if os.path.exists(drive_letter):
            drives.append(drive_letter)
    return drives




def monitor_disk_health(drive_letter):
    try:
        w = wmi.WMI()
        query = f"SELECT * FROM MSStorageDriver_FailurePredictStatus WHERE InstanceName LIKE 'Win32_DiskDrive.DeviceID=\"%s\"'" % (f"PhysicalDrive{drive_letter}")
        results = w.query(query)

        health_status = "Unknown"
        for disk in results:
            if hasattr(disk, "PredictFailure") and disk.PredictFailure:
                health_status = "Failing"
                break
            else:
                health_status = "OK"

        return health_status
    except Exception as e:
        return f"Error: {e}"

def disk_space_usage_analysis(folder_path):
    total_space = psutil.disk_usage(folder_path).total
    used_space = psutil.disk_usage(folder_path).used
    free_space = psutil.disk_usage(folder_path).free

    return {
        'total_space': total_space,
        'used_space': used_space,
        'free_space': free_space
    }

def identify_large_files(folder_path, size_threshold):
    large_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            if file_size > size_threshold:
                large_files.append(file_path)

    return large_files


def get_file_checksum(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
        return hashlib.md5(data).hexdigest()

def identify_duplicate_files(folder_path):
    file_checksums = {}
    duplicate_files = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            checksum = get_file_checksum(file_path)

            if checksum in file_checksums:
                duplicate_files.append((file_checksums[checksum], file_path))
            else:
                file_checksums[checksum] = file_path

    return duplicate_files

def get_file_last_access_time(file_path):
    try:
        last_modified_timestamp = os.path.getmtime(file_path)
        return last_modified_timestamp
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def identify_least_frequently_accessed_files(folder_path, days_threshold):
    print(days_threshold)
    current_time = time.time()
    days_threshold_seconds = days_threshold * 24 * 60 * 60

    least_frequent_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            last_access_time = get_file_last_access_time(file_path)
            print(last_access_time)
            time_difference = current_time - last_access_time
            print(time_difference)
            if time_difference >= days_threshold_seconds:
                least_frequent_files.append((file_path, time_difference / (24 * 60 * 60)))

    return least_frequent_files


def generate_report(folder_path):
    finallist=[]
    # Call all the functions to collect information
    disk_space_usage = disk_space_usage_analysis(folder_path)

    large_files = identify_large_files(folder_path, 100 * 1024 * 1024)  # Example size threshold: 100 MB

    # duplicate_files = find_duplicate_files(folder_path)

    least_frequent_files = identify_least_frequently_accessed_files(folder_path, 90)  # Example days threshold: 90 days

    list.append(disk_space_usage)
    list.append(large_files)
    list.append(least_frequent_files)
    list.append(disk_health_status)
    for drive_letter in get_available_drives():
        disk_health_status ="Disk Health Status for Drive "+drive_letter+ monitor_disk_health(drive_letter)

    # Write the report to a text file
    with open(log_files_path, "w") as f:
        f.write("Disk Space Usage Analysis:\n")
        f.write(f"Total Space: {disk_space_usage['total_space'] / (1024 ** 3):.2f} GB\n")
        f.write(f"Used Space: {disk_space_usage['used_space'] / (1024 ** 3):.2f} GB\n")
        f.write(f"Free Space: {disk_space_usage['free_space'] / (1024 ** 3):.2f} GB\n\n")

        f.write("Large Files:\n")
        for file in large_files:
            f.write(f"- {file} (Size: {os.path.getsize(file) / (1024 ** 2):.2f} MB)\n")
        f.write("\n")

        # f.write("Duplicate Files:\n")
        # for group in duplicate_files:
        #     f.write(f"- Duplicate Group:\n")
        #     for file_path in group:
        #         f.write(f"  - {file_path} (Size: {os.path.getsize(file_path) / (1024 ** 2):.2f} MB)\n")
        # f.write("\n")

        f.write("Least Frequently Accessed Files:\n")
        for file in least_frequent_files:
            f.write(f"- {file} (Last Accessed: {time.ctime(get_file_last_access_time(file))})\n")
        f.write("\n")

        f.write("Disk Health Status:\n")
        f.write(f"{disk_health_status}\n")
        return finallist
    
# Function for disk space scanning and management (Replace this with your actual scanning and management functions)
def scan_and_manage_disk_space():
    print("Running disk space scanning and management...")
    generate_report(folder_path)
    send_old_files_to_archive()
    # Your disk space scanning and management functions go here

def get_scan_interval_from_user():
    while True:
        try:
            interval = int(input("Enter the scan interval in minutes (e.g., 60 for 1 hour): "))
            if interval <= 0:
                print("Please enter a positive interval.")
            else:
                return interval
        except ValueError:
            print("Invalid input. Please enter a valid number.")



# if __name__ == "__main__":
#     # Get the scan interval from the user
#     # interval_minutes = get_scan_interval_from_user()

#     # Schedule the scan_and_manage_disk_space function to run at the specified interval
#     # schedule.every(interval_minutes).minutes.do(scan_and_manage_disk_space)

#     # Print the scheduled interval to the user
#     # print(f"Scheduled disk space scanning and management every {interval_minutes} minutes.")
    
#     # Main loop to run the scheduled tasks
#     # print(identify_least_frequently_accessed_files(folder_path,90))
#     print(identify_least_frequently_accessed_files(r"D:\University\CD",5))
#     # while True:
#         # schedule.run_pending()
#         # time.sleep(1)  # Sleep for 1 second to avoid excessive CPU usage


