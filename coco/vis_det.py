# # Purpose: visualize a folder of images using bbox.json
# import cv2
# import json
# import os
# import numpy as np
# import sys

# # # Define a list of class labels corresponding to the category IDs
# # class_labels = [
# #     "person",
# #     "rider",
# #     "car",
# #     "truck",
# #     "bus",
# #     "train",
# #     "motorcycle",
# #     "bicycle"
# # ]

# # colors = [(100, 170, 30), 
# #         (220, 220, 0), 
# #         (175, 116, 175), 
# #         (250, 0, 30),
# #         (165, 42, 42), 
# #         (255, 77, 255), 
# #         (0, 226, 252), 
# #         (182, 182, 255)]
# # colors = [(0, 0, 128) ]



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


# def main():

#     img_folder = sys.argv[1] # images
#     label_file = sys.argv[2] # bbox.json in bdd format
#     id_filename_mapping_file = sys.argv[3] # ori. label
#     use_text = sys.argv[4].lower() in ['true', '1', 'yes']

#     # NOTE: hardcode this now for pretrained model
#     # Define a list of class labels corresponding to the category IDs
#     class_labels = [
#         "pedestrian",
#         "rider",
#         "car",
#         "truck",
#         "bus",
#         "train",
#         "motorcycle",
#         "bicycle",
#         "traffic light",
#         "traffic sign"
#     ]


#     iou_threshold = 0.50
#     score_threshold = 0.50

#     # Define the path to the output folder
#     # output_folder = label_file.replace('bbox.json', 'visual')
#     # NOTE: change from bbox to coco_instances_results
#     output_folder = label_file.replace('coco_instances_results.json', 'visual')

#     # Load the label data from the COCO format label file
#     with open(label_file, "r") as f:
#         label_data = json.load(f)

#     # Load the mapping data from the id_filename_mapping_file
#     with open(id_filename_mapping_file, "r") as f:
#         mapping_data = json.load(f)

#     # Create a dictionary to map image IDs to file names
#     id_to_filename = {}
#     for img in mapping_data["images"]:
#         id_to_filename[img["id"]] = img["file_name"]

#     # Create a dictionary to map image IDs to their annotations
#     id_to_annotations = {}
#     for ann in label_data:
#         img_id = ann["image_id"]
#         if img_id not in id_to_annotations:
#             id_to_annotations[img_id] = []
#         id_to_annotations[img_id].append(ann)

#     # Loop over the images and draw the annotations on the images
#     success = 0

#     for img_id, annotations in id_to_annotations.items():
#         # Get the file name for the image
#         img_filename = id_to_filename[img_id]

#         # Load the image using OpenCV
#         img_path = os.path.join(img_folder, img_filename)
#         img = cv2.imread(img_path)

#         # Draw the ground truth bounding boxes for the image
#         for ann in mapping_data['annotations']:
#             if ann['image_id'] == img_id:
#                 bbox = ann['bbox']
#                 x, y, w, h = bbox
#                 cv2.rectangle(img, (int(x), int(y)), (int(x + w), int(y + h)), (255, 0, 0), 2) # blue

#         # Loop over the annotations for the image and draw the bounding boxes and labels
#         detections = []
#         for ann in annotations:
#             bbox = ann["bbox"]
#             x, y, w, h = bbox
#             category_id = ann["category_id"]
#             score = ann['score']
#             image_id = ann["image_id"]
            
#             # skip the low-score object 
#             if score < score_threshold:
#                 continue
            
#             # Append the detection to the list
#             detections.append({
#                 'bbox': [x, y, w, h],
#                 'score': score,
#                 'category_id': category_id,
#                 'image_id': image_id
#             })

#         # Apply NMS separately for each image
#         for image_id in set([d['image_id'] for d in detections]):
#             detections_for_image = [d for d in detections if d['image_id'] == image_id]
#             detections_for_image = apply_nms(detections_for_image, iou_threshold)
#             # color_idx = 0

#             for detection in detections_for_image:
#                 bbox = detection["bbox"]
#                 x, y, w, h = bbox
#                 category_id = detection["category_id"]
#                 score = detection['score']

#                 label = f"{class_labels[category_id - 1]}: {score:.2f}"
#                 # color = colors[color_idx % len(colors)]

#                 cv2.rectangle(img, (int(x), int(y)), (int(x + w), int(y + h)), (0, 0, 255),  2) # red
#                 if use_text == True:
#                     cv2.putText(img, label, (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
#                 # color_idx += 1

#             # Save the image with the annotations drawn to the output folder
#             output_path = os.path.join(output_folder, img_filename)
#             os.makedirs(os.path.dirname(output_path), exist_ok=True)
#             cv2.imwrite(output_path, img)

#         success += 1
