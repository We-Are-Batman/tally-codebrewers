import os
import hashlib
from collections import defaultdict
import Levenshtein
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




def main():
    directory_to_scan = r"C:\Users\kabir\OneDrive\Desktop\testing"
    duplicate_files = find_duplicate_files(directory_to_scan)

    if not duplicate_files:
        print("No duplicate files found.")
    else:
        print("Duplicate files:")
        for file_hash, file_paths in duplicate_files.items():
            print(f"Hash: {file_hash}")
            for file_path in file_paths:
                print(f" - {file_path}")

if __name__ == "__main__":
    main()
