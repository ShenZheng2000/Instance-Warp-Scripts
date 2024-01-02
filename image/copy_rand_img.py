import os
import random
import shutil

# Purpose: Copy a random subset of images from one folder to another

# Set random seed
random.seed(0)

# Source folders
folder_A = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k_1_20/trainA"  # Contains .jpg files
folder_B = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k_1_20/trainS"  # Contains .png files

# Destination folders
folder_C = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k_7_20_snowy/trainA"  # Destination for .jpg files
folder_D = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k_7_20_snowy/trainS"  # Destination for .png files

os.makedirs(folder_C, exist_ok=True)
os.makedirs(folder_D, exist_ok=True)

# Number of images to copy
num_images_to_copy = 6259 # NOTE: keep same ratio as clear2rainy experiments

# Get a list of image files in each source folder
images_A = [file for file in os.listdir(folder_A) if file.endswith('.jpg')]
images_B = [file for file in os.listdir(folder_B) if file.endswith('.png')]

assert len(images_A) == len(images_B), f"numbers of images {len(images_A)} and {len(images_B)} mismatched!"

# Randomly select a subset of images from folder A
random_images = random.sample(images_A, min(len(images_A), num_images_to_copy))

# Copy images from Folder A to Folder C and corresponding images from Folder B to Folder D
count = 0
for image in random_images:
    base_name, ext = os.path.splitext(image)
    source_A = os.path.join(folder_A, image)
    destination_C = os.path.join(folder_C, image)

    # change the extension for images in folder B
    image_B = base_name + '.png'
    source_B = os.path.join(folder_B, image_B)
    destination_D = os.path.join(folder_D, image_B)

    shutil.copy2(source_A, destination_C)
    shutil.copy2(source_B, destination_D)
    count += 1

print(f'finished {count} images')
