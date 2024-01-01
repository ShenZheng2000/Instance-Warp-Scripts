import os


def remove_non_model_final_pth(directory, excluded_folder, debug_mode):

    for root, dirs, files in os.walk(directory):
        if excluded_folder in dirs:
            dirs.remove(excluded_folder)  # Exclude the specific folder from further traversal
            print(f"excluded {excluded_folder}")

        for file in files:
            if file.endswith('.pth') and file not in ['instances_predictions.pth', 'model_final.pth']:
                file_path = os.path.join(root, file)
                if debug_mode is False:
                    os.remove(file_path)
                    print(f"Removed: {file_path}")

# Replace 'path_to_directory' and 'excluded_folder' with the actual paths
path_to_directory = '/home/aghosh/Projects/2PCNet/outputs'
excluded_folder = 'cur_TPSeNCE_8_8'
debug_mode = False # NOTE: be careful with this!
remove_non_model_final_pth(path_to_directory, excluded_folder, debug_mode)
