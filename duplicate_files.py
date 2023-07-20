import os
import hashlib
from collections import defaultdict
import difflib
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
                similarity = difflib.SequenceMatcher(None, file1_key, group_key).ratio()
                if similarity >= similarity_threshold:
                    found_group = group_key
                    break

            if found_group is None:
                similar_files[file1_key] = [file1_path]
            else:
                similar_files[found_group].append(file1_path)

    similar_files = {key: value for key, value in similar_files.items() if len(value) > 1}

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
                    similarity = difflib.SequenceMatcher(None, content1, content2).ratio()
                    if similarity >= similarity_threshold:
                        similar_group = group_key
                        break
                if similar_group is not None:
                    break

            if similar_group is None:
                similar_files[file_path] = [file_path]
            else:
                similar_files[similar_group].append(file_path)

    similar_files = {key: value for key, value in similar_files.items() if len(value) > 1}
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
    directory_path=directory
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


directory_path = r"D:\University\Lab\AI\Assignment 4"