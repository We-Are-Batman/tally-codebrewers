import os
import time
import json


extensions = {}

#read from  json file into dictionary

with open('file_association.json') as json_file:
    extensions = json.load(json_file)






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
            if len(file_extension)<1:
                continue
            if file_extension not in extensions:
                actual_type = "documents"
            else:
                actual_type = extensions[file_extension]

            # print(filename,file_extension)
            if file_dict.get(actual_type)==None:
                file_dict[actual_type] = 0

            file_dict[actual_type] = file_dict[actual_type] +  file_stats.st_size

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
drive_path = "C:\\"
files_and_metadata = get_files_and_metadata(drive_path)

for extension,size in files_and_metadata.items():
    tot = float("{:.2f}".format(size / (1024.0)))
    print(f"for extension {extension} size is {tot} KB")