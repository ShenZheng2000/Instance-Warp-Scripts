import os
import shutil

# Define the path to the input folder with images
input_folder = "/home/aghosh/Projects/2PCNet/Datasets/boreas/filtered"

# Define the path to the output folder where you want to save train and test sets
output_folder = "/home/aghosh/Projects/2PCNet/Datasets/boreas/images"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# List all files in the input folder and sort them by name
image_files = sorted(os.listdir(input_folder))

# Calculate the number of images for the train set (80%)
train_size = int(0.8 * len(image_files))

# Create a list of images for the train set
train_images = image_files[:train_size]

# Create a list of images for the test set
test_images = image_files[train_size:]

# Copy the train images to the output folder
for image in train_images:
    source_path = os.path.join(input_folder, image)
    dest_path = os.path.join(output_folder, "train", image)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copyfile(source_path, dest_path)

# Copy the test images to the output folder
for image in test_images:
    source_path = os.path.join(input_folder, image)
    dest_path = os.path.join(output_folder, "test", image)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copyfile(source_path, dest_path)

print("Images sorted and split into train and test sets.")
