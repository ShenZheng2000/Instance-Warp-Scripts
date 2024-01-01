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


# # Purpose: Convert the segmentation maps to bboxes

# import torch

# def extract_bboxes(segmentation_map, ignore_labels=None):
#     if ignore_labels is None:
#         ignore_labels = []

#     # Convert the segmentation map to a PyTorch tensor if it's not already
#     if not isinstance(segmentation_map, torch.Tensor):
#         segmentation_map = torch.tensor(segmentation_map)

#     # Create a mask for the labels that should not be ignored
#     valid_mask = torch.ones_like(segmentation_map, dtype=torch.bool)
#     for label in ignore_labels:
#         valid_mask &= (segmentation_map != label)

#     # Find the non-zero (i.e., valid) coordinates in the tensor
#     y, x = torch.nonzero(valid_mask, as_tuple=True)

#     # Get the min and max coordinates
#     x_min, x_max = x.min(), x.max()
#     y_min, y_max = y.min(), y.max()

#     # Return the bounding box
#     return [(x_min.item(), y_min.item(), x_max.item(), y_max.item())]

# # Sample usage
# segmentation_map = torch.tensor([[0, 0, 0, 0, 0],
#                                  [0, 1, 1, 1, 0],
#                                  [0, 1, 1, 0, 2],
#                                  [0, 0, 0, 2, 2]])

# # Assuming label 0 and 2 are the ones you want to ignore
# ignore_labels = [0, 2]

# bboxes = extract_bboxes(segmentation_map, ignore_labels)
# print(bboxes)  # Outputs: [(1, 1, 3, 2)]