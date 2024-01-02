import os
import json
import shutil

# Purpose: Copy images from a folder to another folder conditioned on a JSON file

# Define the paths to the input folder with images, COCO JSON file, and the output folder
image_folder = "/home/aghosh/Projects/2PCNet/Datasets/dense/cam_stereo_left_lut"
coco_json_file = "/home/aghosh/Projects/2PCNet/Datasets/dense/coco_labels/val_dense_fog.json"
output_folder = "/home/aghosh/Projects/2PCNet/Datasets/dense/cam_stereo_left_lut_fog_val"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the COCO JSON file
with open(coco_json_file, "r") as json_file:
    coco_data = json.load(json_file)

# Extract image filenames from COCO annotations
image_filenames = [entry["file_name"] for entry in coco_data["images"]]

count = 0

# Iterate through the image filenames and copy them if they exist in the input folder
for image_name in image_filenames:
    image_path = os.path.join(image_folder, image_name)
    
    # Check if the image exists in the input folder
    if os.path.exists(image_path):
        # If it exists, copy it to the output folder
        output_path = os.path.join(output_folder, image_name)
        shutil.copyfile(image_path, output_path)
        print(f"Copied: {image_name} to {output_folder}")
        count += 1
    else:
        print(f"Image not found: {image_name}")

print("Done copying images.")
print(f"Total images copied: {count}")
