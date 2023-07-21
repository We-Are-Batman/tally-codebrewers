import os
import zipfile
from datetime import datetime
from file_deletion import delete_files_multithread

def create_zip(file_paths,output_directory ):
    output_zip_filename = 'output_files.zip'
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Generate timestamp
    output_filename_with_timestamp = f"{output_zip_filename}_{timestamp}.zip"

    output_path = os.path.join(output_directory, output_filename_with_timestamp)

    with zipfile.ZipFile(output_path, 'w') as zipf:
        for file_path in file_paths:
            if os.path.isfile(file_path):
                zipf.write(file_path, os.path.basename(file_path))
            else:
                print(f"Warning: '{file_path}' is not a valid file path. Skipping.")

    delete_files_multithread(file_path)
    print(f"Zip file created at '{output_path}'.")

# Example usage:
# file_paths_to_zip = [
#     'E:\\1.jpg',
#     'E:\\2.jpg',
#     # Add more file paths as needed
# ]
# output_directory = "E:\\"


# create_zip(file_paths_to_zip, output_directory)

