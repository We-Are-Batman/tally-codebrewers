import os
import time
import json
import heapq


extensions = {}

#read from  json file into dictionary

with open('file_association.json') as json_file:
    extensions = json.load(json_file)


def get_thresold_elements(path,extension,thresold):
        
    lst = []

    for root, _, files in os.walk(path):
        for filename in files:
            try:            
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
                
                if extension !="*" and extension != actual_type:
                        continue
                
                if file_stats.st_size < thresold:
                     continue
                
                lst.append((filename,file_stats.st_size,file_path))
                
            except:
                 pass

    return lst


drive_path = "C:\\"
thresold = 6000000
extension = "*"

top_files = get_thresold_elements(drive_path,extension,thresold)
for data in top_files:
    print(data)