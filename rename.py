import os

def rename_files_in_directory(directory_path, prefix="", suffix=""):
    # Get list of files in directory
    files = os.listdir(directory_path)
    
    # Iterate over files and rename them
    for old_name in files:
        old_path = os.path.join(directory_path, old_name)
        name, extension = os.path.splitext(old_name)
        new_name = f"{prefix}{name}{suffix}{extension}"
        new_path = os.path.join(directory_path, new_name)
        os.rename(old_path, new_path)

# Example usage
directory_path = "C:\\Users\\Wilbert\\Desktop\\data\\augmented\\theftstaticshear"
rename_files_in_directory(directory_path, prefix="theft", suffix="shear")
