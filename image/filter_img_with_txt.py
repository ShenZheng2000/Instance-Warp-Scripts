import shutil
import os

# Function to copy files from source to target if they exist in a given text file list
def copy_images_from_list(txt_file, source_folder, target_folder):
    # Create target folder if it doesn't exist
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    # Read the text file line by line
    with open(txt_file, 'r') as file:
        for line in file:
            # Strip removes any leading/trailing whitespace (including new line char)
            basename = line.strip()
            # Construct full source file path
            source_file = os.path.join(source_folder, basename)
            
            # Check if the file exists in the source folder
            if os.path.isfile(source_file):
                # Construct full target file path
                target_file = os.path.join(target_folder, basename)
                # Copy the file to the target folder
                shutil.copy(source_file, target_file)
                print(f"Copied {basename} to {target_folder}")
            else:
                print(f"File {basename} does not exist in the source folder.")

# Example usage:
txt_file = '/home/aghosh/Projects/2PCNet/Scripts/bdd/val/daytime.txt'  # The text file with the basenames
source_folder = '/home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/100k/val'  # Replace with your source folder path
target_folder = '/home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/100k/val_day'  # Replace with your target folder path

copy_images_from_list(txt_file, source_folder, target_folder)
