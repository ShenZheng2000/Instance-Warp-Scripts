# Purpose: visualize a folder of images using bbox.json
import cv2
import json
import os
import numpy as np
import sys

def iou(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # Determine the coordinates of the intersection rectangle
    x_left = max(x1, x2)
    y_top = max(y1, y2)
    x_right = min(x1 + w1, x2 + w2)
    y_bottom = min(y1 + h1, y2 + h2)

    # If the boxes do not intersect, return 0
    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # Compute the area of intersection rectangle
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # Compute the area of both rectangles
    box1_area = w1 * h1
    box2_area = w2 * h2

    # Compute the IOU
    iou = intersection_area / float(box1_area + box2_area - intersection_area)

    return iou


def apply_nms(boxes, iou_thresh):
    """
    Applies non-maximum suppression (NMS) to the input boxes.

    Args:
        boxes (list): A list of dictionaries, each representing a bounding box and its score.
            Each dictionary has the following keys:
                - bbox (list): A list of 4 integers representing the box coordinates (x, y, width, height).
                - score (float): The score/confidence of the box.
        iou_thresh (float): The IoU threshold to use for NMS.

    Returns:
        A list of dictionaries representing the boxes after NMS has been applied. Each dictionary has the same keys
        as the input dictionaries.
    """
    # Sort boxes by their score in descending order
    boxes = sorted(boxes, key=lambda x: x['score'], reverse=True)

    # Initialize the list of selected boxes and loop over all the boxes
    selected_boxes = []
    for box in boxes:
        # Check if the current box overlaps with any of the selected boxes above the IoU threshold
        if not any(iou(box['bbox'], sel_box['bbox']) > iou_thresh for sel_box in selected_boxes):
            selected_boxes.append(box)

    return selected_boxes


img_folder = sys.argv[1] # images
label_file = sys.argv[2] # bbox.json in bdd format
id_filename_mapping_file = sys.argv[3] # ori. label
# use_text = sys.argv[4].lower() in ['true', '1', 'yes']
'''
Example run:
python vis_det_each.py \
    /home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/100k/val \
    /longdata/anurag_storage/2PCNet/outputs_11_14_det_ckpts/bdd100k_9_22_v1/night/inference/coco_instances_results.json \
    /home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_night.json
'''


use_text = True

# NOTE: hardcode this now for pretrained model
# Define a list of class labels corresponding to the category IDs
class_labels = [
    "pedestrian", "rider", "car",
    "truck", "bus", "train",
    "motorcycle", "bicycle", "traffic light",
    "traffic sign"
]

# This is from colorbrew
colormap = [
    (141,211,199),
    (255,255,179),
    (190,186,218),
    (251,128,114),
    (128,177,211),
    (253,180,98),
    (179,222,105),
    (252,205,229),
    (217,217,217),
    (188,128,189),
]


# Old function => smaller font size
# def add_text_with_black_background(image, label, position, font_scale, font_color, bg_color):
#     text_size, baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 1)
#     cv2.rectangle(image, (position[0], position[1] - text_size[1] - 5), (position[0] + text_size[0], position[1]), bg_color, -1)
#     cv2.putText(
#         img=image,
#         text=label,
#         org=position,
#         fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#         fontScale=font_scale,
#         color=font_color,
#         thickness=1
#     )

# New function => This one looks nice!!!!!!!!!!!!
def add_text_with_black_background(image, label, position, base_font_scale=1.5, font_color=None, bg_color=(0,0,0), base_padding=5, base_thickness=3):
    # Determine the scaling factor based on image resolution
    base_resolution = (2048, 1080)  # Base resolution for 2K
    current_resolution = image.shape[1], image.shape[0]  # Width, Height
    scale_factor = min(current_resolution[0] / base_resolution[0], current_resolution[1] / base_resolution[1])

    # Scale font size, padding, and thickness
    font_scale = base_font_scale * scale_factor
    padding = int(base_padding * scale_factor)
    thickness = base_thickness # NOTE: do not scale thickness

    # Calculate text size with the scaled font size and thickness
    text_size, baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)

    # Increase the size of the background box with padding
    bg_box_top_left = (position[0], position[1] - text_size[1] - padding)
    bg_box_bottom_right = (position[0] + text_size[0] + padding, position[1] + padding)

    # Draw the background box
    cv2.rectangle(image, bg_box_top_left, bg_box_bottom_right, bg_color, -1)

    # Draw the text
    cv2.putText(
        img=image,
        text=label,
        org=(position[0] + padding // 2, position[1] - padding // 2),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=font_scale,
        color=font_color,
        thickness=thickness
    )


iou_threshold = 0.50
score_threshold = 0.50

# Define the path to the output folder
# output_folder = label_file.replace('bbox.json', 'visual')
# NOTE: change from bbox to coco_instances_results
output_folder_pred = label_file.replace('coco_instances_results.json', 'visual')
output_folder_gt = label_file.replace('coco_instances_results.json', 'visual_gt')

# Load the label data from the COCO format label file
with open(label_file, "r") as f:
    label_data = json.load(f)

# Load the mapping data from the id_filename_mapping_file
with open(id_filename_mapping_file, "r") as f:
    mapping_data = json.load(f)

# Create a dictionary to map image IDs to file names
id_to_filename = {}
for img in mapping_data["images"]:
    id_to_filename[img["id"]] = img["file_name"]

# Create a dictionary to map image IDs to their annotations
id_to_annotations = {}
for ann in label_data:
    img_id = ann["image_id"]
    if img_id not in id_to_annotations:
        id_to_annotations[img_id] = []
    id_to_annotations[img_id].append(ann)




# Loop over the images and draw the annotations on the images
success = 0

for img_id, annotations in id_to_annotations.items():


    # Get the file name for the image
    img_filename = id_to_filename[img_id]

    # Load the image using OpenCV
    img_path = os.path.join(img_folder, img_filename)
    img = cv2.imread(img_path)

    # Create copies of the image for ground truth and predicted bboxes
    img_gt = img.copy()  # for ground truth bboxes
    img_pred = img.copy()  # for predicted bboxes



    # Draw the ground truth bounding boxes on img_gt
    for ann in mapping_data['annotations']:
        if ann['image_id'] == img_id:
            bbox = ann['bbox']
            category_id = ann['category_id']
            x, y, w, h = bbox
            color = colormap[category_id - 1]  # Use color from colormap
            cv2.rectangle(img_gt, (int(x), int(y)), (int(x + w), int(y + h)), color, 2)

            # Optionally add labels
            if use_text == True:
                label = f"{class_labels[category_id - 1]}"
                text_color = color  # Use the same color as the bounding box
                text_bg_color = (0, 0, 0)  # Black background color
                add_text_with_black_background(
                    image=img_gt,
                    label=label,
                    position=(int(x), int(y) - 5),
                    # font_scale=0.7,
                    # font_scale=1.5,
                    font_color=text_color,
                    bg_color=text_bg_color,
                )


    # Loop over the annotations for the image and draw the bounding boxes and labels
    # Initialize a list for detections
    detections = []
    for ann in annotations:
        bbox = ann["bbox"]
        score = ann['score']
        category_id = ann["category_id"]
        image_id = ann["image_id"]

        # Skip low-score objects
        if score < score_threshold:
            continue

        # Append the detection to the list
        detections.append({
            'bbox': bbox,
            'score': score,
            'category_id': category_id,
            'image_id': image_id
        })




    # Apply NMS separately for each image
    for image_id in set([d['image_id'] for d in detections]):
        detections_for_image = [d for d in detections if d['image_id'] == image_id]
        detections_for_image = apply_nms(detections_for_image, iou_threshold)

        # Draw bounding boxes that passed NMS
        for detection in detections_for_image:
            bbox = detection["bbox"]
            x, y, w, h = bbox
            category_id = detection["category_id"]
            score = detection['score']

            color = colormap[category_id - 1]  # Get color based on category_id
            cv2.rectangle(img_pred, (int(x), int(y)), (int(x + w), int(y + h)), color, 2)

            # Optionally add labels
            if use_text == True:
                label = f"{class_labels[category_id - 1]}: {score:.2f}"
                text_color = color  # Use the same color as the bounding box
                text_bg_color = (0, 0, 0)  # Black background color
                add_text_with_black_background(
                    image=img_pred,
                    label=label,
                    position=(int(x), int(y) - 5),
                    # font_scale=0.7,
                    # font_scale=1.5,
                    font_color=text_color,
                    bg_color=text_bg_color,
                )


    # Save the image with ground truth bboxes
    output_path_gt = os.path.join(output_folder_gt, img_filename)  # Define output_folder_gt
    os.makedirs(os.path.dirname(output_path_gt), exist_ok=True)
    cv2.imwrite(output_path_gt, img_gt)

    # Save the image with predicted bboxes
    output_path_pred = os.path.join(output_folder_pred, img_filename)  # Define output_folder_pred
    os.makedirs(os.path.dirname(output_path_pred), exist_ok=True)
    cv2.imwrite(output_path_pred, img_pred)

    success += 1

    if success % 100 == 0:
        print(f"Processed {success} images")






