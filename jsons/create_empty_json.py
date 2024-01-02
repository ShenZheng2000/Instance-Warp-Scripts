import json
import os
import sys
from PIL import Image

# Purpose: Create an empty JSON file for COCO-style annotations

# Define the structure of the JSON file
coco_data = {
    "info": {},
    "licenses": [],
    "images": [],
    "annotations": [],
    "categories": [
        {
            "supercategory": "none",
            "id": 1,
            "name": "pedestrian"
        },
        {
            "supercategory": "none",
            "id": 2,
            "name": "rider"
        },
        {
            "supercategory": "none",
            "id": 3,
            "name": "car"
        },
        {
            "supercategory": "none",
            "id": 4,
            "name": "truck"
        },
        {
            "supercategory": "none",
            "id": 5,
            "name": "bus"
        },
        {
            "supercategory": "none",
            "id": 6,
            "name": "train"
        },
        {
            "supercategory": "none",
            "id": 7,
            "name": "motorcycle"
        },
        {
            "supercategory": "none",
            "id": 8,
            "name": "bicycle"
        },
        {
            "supercategory": "none",
            "id": 9,
            "name": "traffic light"
        },
        {
            "supercategory": "none",
            "id": 10,
            "name": "traffic sign"
        }
        
    ]
}


weather = 'foggy'
time = 'day'

images_folder = f"/home/aghosh/Projects/2PCNet/Datasets/gm/{weather}/{time}/images"  # Replace with the actual path
output_json_path = f"/home/aghosh/Projects/2PCNet/Datasets/gm/coco_labels/{weather}_{time}.json"  # Replace with desired output path


# Loop through all the subfolders and image files in the folder
for subdir, dirs, files in os.walk(images_folder):
    for filename in files:
        if filename.endswith((".jpg", ".png")):
            # Get the image size
            img_path = os.path.join(subdir, filename)

            # Open the image and get its size
            with Image.open(img_path) as img:
                width, height = img.size

            # Add the image information to the JSON file
            image_id = len(coco_data["images"]) + 1
            image_info = {
                "id": image_id,
                "file_name": os.path.relpath(img_path, images_folder),  # relative path from images_folder
                "height": height,
                "width": width
            }
            coco_data["images"].append(image_info)


# Save the JSON file
with open(output_json_path, "w") as f:
    json.dump(coco_data, f, indent=4)

