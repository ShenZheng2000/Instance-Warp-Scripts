import os
import json
import shutil

# Purpose: Filter images in a folder based on a JSON file

# Function to read Coco format JSON file and get the list of image filenames
def read_json_file(json_file_path):
    with open(json_file_path, 'r') as f:
        coco_data = json.load(f)
    return [image['file_name'] for image in coco_data['images']]

# Function to filter images in a folder based on the JSON file
def filter_images(json_file_path, image_folder_path, output_folder_path):
    image_filenames = read_json_file(json_file_path)
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    count = 0
    for filename in os.listdir(image_folder_path):
        if filename in image_filenames:
            src_path = os.path.join(image_folder_path, filename)
            dst_path = os.path.join(output_folder_path, filename)
            shutil.copy(src_path, dst_path)
            count += 1

    print(f"finished {count} images")

if __name__ == "__main__":
    # Replace these paths with your actual file paths
    json_file_path = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_rainy.json"
    image_folder_path = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/100k/val"
    output_folder_path = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/val_rainy"

    filter_images(json_file_path, image_folder_path, output_folder_path)
