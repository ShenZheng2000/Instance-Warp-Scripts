import cv2
import json
import os


import cv2
import numpy as np

# Define the path to the JSON file containing vanishing point coordinates
vanishing_points_file = "/home/aghosh/Projects/2PCNet/Datasets/VP/bdd100k_all_vp.json"

# Load the vanishing point data from the JSON file into a Python dictionary
with open(vanishing_points_file, "r") as f:
    vanishing_points_data = json.load(f)

# Define the path to the input image
# image_path = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/100k/train_debug/0a0b16e2-93f8c456.jpg"
# image_path = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/100k/train_debug/0a0cc110-7f2fd761.jpg"
# image_path = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/100k/train_debug/0a0eebd9-b6fff9e2.jpg"
image_path = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/100k/train_debug/0a2a1a40-44173767.jpg"

# Extract the image's base name to search for the corresponding vanishing point
image_basename = os.path.basename(image_path)

# Initialize vanishing point coordinates
vp_x, vp_y = None, None

# Traverse all keys in the JSON data
for key, value in vanishing_points_data.items():
    if key.endswith(image_basename):
        vp_x, vp_y = value
        break

# Check if the vanishing point coordinates are found
if vp_x is not None and vp_y is not None:
    # Load the image
    image = cv2.imread(image_path)

    # Draw a blurred dot at the vanishing point
    image_with_vp = image.copy()
    cv2.circle(image_with_vp, (int(vp_x), int(vp_y)), 10, (0, 0, 255), -1)  # Red dot

    # Save the image with the vanishing point
    output_image_path = image_path.replace(".jpg", "_with_vp.jpg")
    cv2.imwrite(output_image_path, image_with_vp)

    print(f"Vanishing point drawn and saved as {output_image_path}")
else:
    print(f"No vanishing point data found for {image_basename}")