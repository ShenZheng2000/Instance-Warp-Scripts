import os
import shutil
import sys

def remove_duplicates(folder_a_path, folder_b_path):
    folder_a_files = set(os.listdir(folder_a_path))
    folder_b_files = os.listdir(folder_b_path)

    for filename in folder_b_files:
        if filename in folder_a_files:
            file_path = os.path.join(folder_b_path, filename)
            os.remove(file_path)
            print(f"Removed {filename} from folder B.")

if __name__ == "__main__":
    surfix = sys.argv[1]
    folder_a_path = f"/home/aghosh/Projects/2PCNet/Methods/TPSeNCE/results/test/bdd100k_7_19_night_tri_sem/test_latest/images/{surfix}"
    folder_b_path = f"/home/aghosh/Projects/2PCNet/Methods/TPSeNCE/results/train/bdd100k_7_19_night_tri_sem/test_latest/images/{surfix}"

    remove_duplicates(folder_a_path, folder_b_path)