# def identify_file_extension(file_path):
#     # Dictionary of file signatures and corresponding file extensions
#     file_signatures = {
#         # Images
#         b"\xFF\xD8\xFF\xE0": ".jpg",
#         b"\xFF\xD8\xFF\xE1": ".jpg",
#         b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A": ".png",
#         b"\x47\x49\x46\x38": ".gif",
#         b"\x42\x4D": ".bmp",
#         b"\x00\x00\x01\x00": ".ico",
#         b"\x49\x49\x2A\x00": ".tiff",
#         b"\x4D\x4D\x00\x2A": ".tiff",

#         # Documents
#         b"\x25\x50\x44\x46": ".pdf",
#         b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1": ".docx",
#         b"\x09\x08\x10\x00\x00\x06\x05\x00": ".vsdx",
#         b"\x50\x4B\x03\x04": ".zip",
#         b"\x50\x4B\x05\x06": ".zip",
#         b"\x50\x4B\x07\x08": ".zip",
#         b"\x50\x4B\x4C\x49\x54\x55": ".zip",
#         b"\x4D\x5A": ".exe",
#         b"\x7F\x45\x4C\x46": ".elf",

#         # Audio/Video
#         b"\x66\x74\x79\x70\x69\x73\x6F\x6D": ".mid",
#         b"\x4F\x67\x67\x53": ".ogg",
#         b"\x49\x44\x33": ".mp3",
#         b"\x66\x4C\x61\x43": ".flac",
#         b"\x52\x49\x46\x46": ".wav",
#         b"\x1A\x45\xDF\xA3": ".webm",
#         b"\x00\x00\x00\x18\x66\x74\x79\x70\x33\x67\x70": ".mp4",
#         b"\x30\x26\xB2\x75\x8E\x66\xCF\x11\xA6\xD9\x00\xAA\x00\x62\xCE\x6C": ".wmv",
#         b"\x2E\x52\x4D\x46": ".rm",

#         # Archives/Compressed
#         b"\x37\x7A\xBC\xAF\x27\x1C": ".7z",
#         b"\x1F\x8B\x08": ".gz",
#         b"\x42\x5A\x68": ".bz2",
#         b"\x50\x4B\x03\x04": ".zip",
#         b"\x50\x4B\x05\x06": ".zip",
#         b"\x52\x61\x72\x21\x1A\x07\x00": ".rar",
#         b"\x50\x4B\x07\x08": ".zip",
#         b"\x50\x4B\x4C\x49\x54\x55": ".zip",

#         # Programming
#         b"\xEF\xBB\xBF": ".txt",
#         b"\xFF\xFE": ".txt",
#         b"\xFE\xFF": ".txt",
#         b"\x23\x21\x2F\x62\x69\x6E": ".sh",
#         b"\x23\x20\x64\x65\x66\x69\x6E\x65": ".sh",
#     }

#     try:
#         # Read the first few bytes of the file
#         with open(file_path, "rb") as file:
#             file_signature = file.read(16)

#         print(file_signature)
#         # Match the file signature with known signatures
#         for signature, extension in file_signatures.items():
#             if file_signature.startswith(signature):
#                 return extension

#         # If no match found, return ".dat" as the default extension
#         return ".dat"

#     except:
#         return ".dat"

import magic
import re

def extract_extension_from_file_type(file_type):
    # Regular expression to extract the extension from file type
    extension_pattern = r'(?i)\b(jpeg|png|gif|bmp|ico|tiff|webp|pdf|zip|mp3|ogg|wav|webm|mp4|exe|elf|7z|gz|bz2|rar|txt|sh)\b'
    match = re.search(extension_pattern, file_type)
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


