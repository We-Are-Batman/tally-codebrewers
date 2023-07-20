import os
import time
import json
import heapq


extensions = {}

#read from  json file into dictionary

with open('file_association.json') as json_file:
    extensions = json.load(json_file)


def get_top_k_elements(path,extension,k):
        
    heap = []

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
                
                # print(filename,file_stats.st_size)
                heapq.heappush(heap, (file_stats.st_size, (filename,file_stats.st_size,file_path)))
                if len(heap) > k:
                        heapq.heappop(heap)[1]
            except:
                 pass

    ans = []
    for priority,data in heap:
         ans.append(data)
    return ans[::-1]


drive_path = "C:\\"
k = 5
extension = "*"

top_files = get_top_k_elements(drive_path,extension,k)
for data in top_files:
    print(data)