import magic
import re

def extract_extension_from_file_type(file_type):
    # Regular expression to extract the extension from file type
    extension_pattern = r'(?i)\b(jpeg|png|gif|bmp|ico|tiff|webp|pdf|zip|mp3|ogg|wav|webm|mp4|exe|elf|7z|gz|bz2|rar|txt|sh)\b'
    match = re.search(extension_pattern, file_type)
    # print(match)
    return f".{match.group(1).lower()}" if match else None

def identify_file_extension(file_path):
    try:
        # Create a magic object
        file_magic = magic.Magic()

        # Get the file type
        file_type = file_magic.from_file(file_path)

        # Extract the extension from the file type
        extension = extract_extension_from_file_type(file_type)

        return extension if extension else ".dat"

    except FileNotFoundError:
        return ".dat"
    except Exception as e:
        return f"Error identifying file extension: {e}"

# if __name__ == "__main__":
#     file_path = "C:\\Users\\ACER\\Pictures\\Camera Roll\\WIN_20230721_18_03_16_Pro.mp4"  
#     file_extension = identify_file_extension(file_path)
#     print(f"The file extension is: {file_extension}")


