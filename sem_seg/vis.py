# Purpose: visualize a simple format bboxes on an image

import cv2
import numpy as np
import json
import os

target_image_full_path = "/home/aghosh/Projects/2PCNet/Datasets/synthia/RGB/0001000.png"

# Replace with your JSON file path
json_file_path = '/home/aghosh/Projects/2PCNet/Datasets/synthia_seg2det_gt.json'

# Load bounding boxes from JSON file
with open(json_file_path, 'r') as file:
    bounding_boxes = json.load(file)

# Check if the target image is in the JSON data
target_image_basename = os.path.basename(target_image_full_path)

# Check if the basename of the target image is in the JSON data
if target_image_basename in bounding_boxes:
    # Read the image
    image = cv2.imread(target_image_full_path)

    # Draw bounding boxes
    for bbox in bounding_boxes[target_image_basename]:
        x1, y1, x2, y2 = bbox
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box with thickness 2

    # Prepare the path to save the visualized image
    # Appending '_visualized' to the original filename
    visualized_image_path = 'visualized.png'

    # Save the visualized image
    cv2.imwrite(visualized_image_path, image)
    print(visualized_image_path)
    exit()

else:
    print("The specified image is not in the JSON file.")
