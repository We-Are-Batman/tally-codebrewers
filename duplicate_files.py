import os
import hashlib
from collections import defaultdict
import difflib
import filecmp
from file_deletion import delete_files_multithread
#this will return the has for a particular file based on it's content
def get_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def find_duplicate_files(directory):
    file_hashes = defaultdict(list)
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_hash = get_file_hash(file_path)
            file_hashes[file_hash].append(file_path)

    return {file_hash: paths for file_hash, paths in file_hashes.items() if len(paths) > 1}


def find_similar_filenames(directory, similarity_threshold=0.85):
    similar_files = {}

    for root, _, files in os.walk(directory):
        for file1 in files:
            file1_path = os.path.join(root, file1)
            file1_key = file1.lower()

            found_group = None
            for group_key, group_files in similar_files.items():
                similarity = difflib.SequenceMatcher(
                    None, file1_key, group_key).ratio()
                if similarity >= similarity_threshold:
                    found_group = group_key
                    break

            if found_group is None:
                similar_files[file1_key] = [file1_path]
            else:
                similar_files[found_group].append(file1_path)

    similar_files = {key: value for key,
                     value in similar_files.items() if len(value) > 1}

    return similar_files


def find_similar_files(directory, similarity_threshold=0.85):
    similar_files = {}

    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content1 = f.read()

            similar_group = None
            for group_key, group_files in similar_files.items():
                for file2_path in group_files:
                    with open(file2_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content2 = f.read()
                    similarity = difflib.SequenceMatcher(
                        None, content1, content2).ratio()
                    if similarity >= similarity_threshold:
                        similar_group = group_key
                        break
                if similar_group is not None:
                    break

            if similar_group is None:
                similar_files[file_path] = [file_path]
            else:
                similar_files[similar_group].append(file_path)

    similar_files = {key: value for key,
                     value in similar_files.items() if len(value) > 1}
    return similar_files


def duplicatefiles(directory):
    directory_to_scan = directory
    duplicate_files = find_duplicate_files(directory_to_scan)

    if not duplicate_files:
        print("No duplicate files found.")
    else:
        print("Duplicate files:")
        for file_hash, file_paths in duplicate_files.items():
            print(f"Hash: {file_hash}")
            for file_path in file_paths:
                print(f" - {file_path}")


def similarfiles(directory):
    directory_path = directory
    similar_files = find_similar_filenames(directory_path)

    if not similar_files:
        print("No files with similar names found.")
    else:
        print("Files with similar names:")
        for file_key, file_paths in similar_files.items():
            print(f"Similar group for filename '{file_key}':")
            for file_path in file_paths:
                print(f" - File: {os.path.basename(file_path)}")
                print(f"   Path: {file_path}")
            print()


def files_with_similar_content(directory_path):

    similar_files = find_similar_files(directory_path)

    if not similar_files:
        print("No files with identical or similar content found.")
    else:
        print("Files with identical or similar content:")
        for file_key, file_paths in similar_files.items():
            print(f"Identical or similar files for '{file_key}':")
            for file_path in file_paths:
                print(f" - File: {os.path.basename(file_path)}")
                print(f"   Path: {file_path}")
            print()


def get_file_metadata(file_path):
    try:
        # file_stat = os.stat(file_path)
        metadata = {
            "file_size": os.path.getsize(file_path),
            "creation_time": int(os.path.getctime(file_path)),
            "modification_time": int(os.path.getmtime(file_path))
        }
        # print(metadata)
        return metadata
    except Exception as e:
        print(f"Error reading metadata for {file_path}: {e}")
        return None


def metadata_matches(metadata1, metadata2):
    # check for one paramteter here
    return any(metadata1[key] == metadata2[key] for key in metadata1)


def identify_similar_files(directory):
    file_metadata_dict = {}
    similar_files = []

    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            metadata = get_file_metadata(file_path)
            if metadata:
                file_metadata_dict[file_path] = metadata

    for file1, metadata1 in file_metadata_dict.items():
        for file2, metadata2 in file_metadata_dict.items():
            if file1 != file2 and metadata_matches(metadata1, metadata2) and metadata1["file_size"] == metadata2["file_size"]:
                similar_files.append((file1, file2))

    return similar_files


def identicalFilesbasedOnMetadata(directory_to_scan):
    # print("Helo")
    similar_files = identify_similar_files(directory_to_scan)
    # print("Hello")
    if not similar_files:
        print("No similar files found.")
    else:
        print("Similar files:")
        for file_pair in similar_files:
            print(file_pair)



def get_most_recent_file(file_paths):
    most_recent_file = None
    most_recent_time = 0

    for file_path in file_paths:
        try:
            access_time = os.path.getatime(file_path)
            if access_time > most_recent_time:
                most_recent_time = access_time
                most_recent_file = file_path
        except Exception as e:
            print(f"Error getting access time for {file_path}: {e}")

    return most_recent_file

def automaticDeletion(duplicate_files):
    filepaths=[]
    for file_hash, file_paths in duplicate_files.items():
        
            print(f"Hash: {file_hash}")

            file_to_keep=get_most_recent_file(file_paths)
            for file_path in file_paths:
                print(f" - {file_path}")
                if file_path != file_to_keep:
                    filepaths.append(file_path)
    delete_files_multithread(filepaths)

def manualDeletion(duplicate_files):
    filepaths=[]
    for file_hash, file_paths in duplicate_files.items():
        
            print(f"Hash: {file_hash}")
            i=1
            mp={}
            for file_path in file_paths:
                print(f"{i} - {file_path}")
                mp[i]=file_path
                i=i+1
            index=int(input("Select the file number you want to keep"))
            print(mp)
            file_to_keep=mp[index]

            for file_path in file_paths:
                print(f" - {file_path}")
                if file_path != file_to_keep:
                    filepaths.append(file_path)
    delete_files_multithread(filepaths)

def deleteDuplicateFiles(directory_path):
    duplicate_files = find_duplicate_files(directory_path)
    
    if not duplicate_files:
        print("No duplicate files found.")
    else:
        print("Duplicate files:")
        
        print(duplicate_files)

        choice=int(input("Do you want to choose the file to keep or do it automatically?"))
        if choice==1:
            automaticDeletion(duplicate_files)
        elif choice==2:
            manualDeletion(duplicate_files)



directory_path = r"C:\Users\kabir\OneDrive\Desktop\testfile"
deleteDuplicateFiles(directory_path)