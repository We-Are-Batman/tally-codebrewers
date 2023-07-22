import os
import difflib

def create_file_if_not_exists(file_path):
    if not os.path.exists(file_path):
        try:
            with open(file_path, 'w') as file:
                print(f"File '{file_path}' created successfully.")
        except Exception as e:
            print(f"Error creating file: {e}")


def merge_text_files(file1_path, file2_path):
    try:
        with open(file1_path, 'r') as file1:
            file1_content = file1.readlines()

        with open(file2_path, 'r') as file2:
            file2_content = file2.readlines()

        
        
        merged_content = []
        for i in range(max(len(file1_content), len(file2_content))):
            line_file1 = file1_content[i].strip() if i < len(file1_content) else ''
            line_file2 = file2_content[i].strip() if i < len(file2_content) else ''
            clean_line_file1 = line_file1.strip()
            clean_line_file2 = line_file2.strip()

            #out of both we append the line which is not empty
            if clean_line_file2:
                merged_content.append(line_file2)
            elif clean_line_file1:
                merged_content.append(line_file1)

        merged_content = [line + '\n' for line in merged_content]
        with open(file2_path, 'w') as file2:
            file2.writelines(merged_content)
        print("Files merged successfully.")
        os.remove(file1_path)
        # os.remove(file2_path)
    except Exception as e:
        print(f"Error merging files: {e}")


def merge_list_of_text_files(file_paths, output_file):
    if(len(file_paths)<2):
        print("Please select atleast 2 files")        

    else:
        create_file_if_not_exists(output_file)
        file_paths.append(output_file)
        for i in range(1,len(file_paths)):
            print(file_paths[i],file_paths[i-1])
            merge_text_files(file_paths[i-1],file_paths[i])
    

        
# if __name__ == "__main__":
#     file1_path = r"C:\Users\kabir\OneDrive\Desktop\testfile\mergetestfile1.txt"
#     file2_path = r"C:\Users\kabir\OneDrive\Desktop\testfile\mergetestfile2.txt"
#     file3_path = r"C:\Users\kabir\OneDrive\Desktop\testfile\mergetestfile3.txt"
#     file4_path = r"C:\Users\kabir\OneDrive\Desktop\testfile\mergetestfile4.txt"
#     output_file_path = r"C:\Users\kabir\OneDrive\Desktop\testfile\merged.txt"

#     # merge_text_files(file1_path, file2_path, output_file_path)
#     merge_list_of_text_files([file1_path,file2_path,file3_path,file4_path],output_file_path)
#     # Replace file1.txt and file2.txt with the merged content

    
