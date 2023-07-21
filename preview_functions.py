import os
import platform
import subprocess

def preview_file(file_path):
    try:
        if platform.system() == "Windows":
            
            os.startfile(file_path)
        else:
            subprocess.call(["xdg-open", file_path])
    except Exception as e:
        print(f"Error opening file: {e}")

if __name__ == "__main__":
    file_path = r"C:\Users\kabir\OneDrive\Desktop\FINAL450.xlsx"  # Replace with the actual file path

    preview_file(file_path)