import os
import time


extensions = {}

# read from file_association.json and put it in a set



def get_files_and_metadata(folder_path):
    # file_list = []
    file_dict = {}

    for root, _, files in os.walk(folder_path):
        # print(root)
        for filename in files:
            file_path = os.path.join(root, filename)
            file_stats = os.stat(file_path)
            split_tup = os.path.splitext(filename)
            file_extension = split_tup[1]
            # print(filename,file_extension)
            if  file_dict.get(file_extension)==None and len(file_extension)>1:
                file_dict[file_extension] = 0
            if len(file_extension)>1 :
                file_dict[file_extension] = file_dict[file_extension] +  file_stats.st_size

            # file_info = {
            #     "name": filename,
            #     "path": file_path,
            #     "size_bytes": file_stats.st_size,
            #     "last_modified": time.ctime(file_stats.st_mtime),
            #     "created": time.ctime(file_stats.st_ctime),
            # }
            # file_dict.get(file_extension).append(file_info)
            # file_list.append(file_info)

    # print(file_dict)

    return file_dict

# Replace "C:\Your\Drive\Path" with the drive path you want to scan.
drive_path = "F:\\"
files_and_metadata = get_files_and_metadata(drive_path)

for extension,size in files_and_metadata.items():
    print(f"for extension {extension} size is {size} bytes")