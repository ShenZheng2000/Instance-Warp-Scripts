import cv2
import numpy as np
import os
import json
import glob
from tqdm import tqdm

# Path to the folder containing images
folder_path = "/home/aghosh/Projects/2PCNet/Datasets/synthia/RGB"

# JSON output file (NOTE: mut be gt suffix!!!!)s
output_json_file = "/home/aghosh/Projects/2PCNet/Datasets/synthia_seg2det_gt.json"

# Dictionary to hold image paths and their corresponding bounding boxes
bounding_boxes = {}

# image numbers for debug
# debug_count = 5

# Iterate over all PNG images in the folder
for image_file in tqdm(
                    glob.glob(os.path.join(folder_path, '*.png'))
                    ):

    # Replace with appropriate paths for your project
    seg_gt_path = image_file.replace("RGB", "GT/LABELS")
    # print(seg_gt_path)
    # exit()
    # seg_id_path = image_file.replace("RGB", "GT/LABELS")

    seg_gt = cv2.imread(seg_gt_path, cv2.IMREAD_UNCHANGED)
    seg_gt = seg_gt[:, :, ::-1]
    # im = cv2.imread(image_file)

    # channel for instance ids
    seg_instances = seg_gt[:, :, 1]

    # get the ids of unique instances
    instance_ids = np.unique(seg_instances)
    image_bboxes = []

    for instance_id in instance_ids:
        if instance_id == 0:
            continue
        ys, xs = np.where(seg_instances == instance_id)

        y1, y2 = np.min(ys), np.max(ys)
        x1, x2 = np.min(xs), np.max(xs)

        w = x2 - x1
        h = y2 - y1

        if w == 0 or h == 0:
            continue

        # Append bounding box to the list
        # image_bboxes.append([x1, y1, x2, y2])
        # NOTE: must append in int() format!!!
        image_bboxes.append([int(x1), int(y1), int(x2), int(y2)])

    # Add bounding boxes to the dictionary
    base_name = os.path.basename(image_file)
    bounding_boxes[base_name] = image_bboxes
    # bounding_boxes[image_file] = image_bboxes

# Write the dictionary to a JSON file
with open(output_json_file, 'w') as f:
    json.dump(bounding_boxes, f, indent=4)




# im_id = "0000700"
# seg_gt_path = f"/home/aghosh/Projects/2PCNet/Datasets/synthia/GT/LABELS/{im_id}.png"
# seg_id_path = f"/home/aghosh/Projects/2PCNet/Datasets/synthia/GT/LABELS/{im_id}_labelTrainIds.png"

# im_path = f"/home/aghosh/Projects/2PCNet/Datasets/synthia/RGB/{im_id}.png"

# seg_gt = cv2.imread(seg_gt_path, cv2.IMREAD_UNCHANGED)
# seg_gt = seg_gt[:, :, ::-1]
# # seg_id = cv2.imread(seg_id_path)
# im = cv2.imread(im_path)

# ## channel for classes
# seg_classes = seg_gt[:, :, 0]

# ## channel for instance ids
# seg_instances = seg_gt[:, :, 1]

# ## get the ids of unique instances
# instance_ids = np.unique(seg_instances)

# for instance_id in instance_ids:
#     if instance_id == 0:
#         continue
#     ys, xs = np.where(seg_instances == instance_id)
#     y1, y2 = np.min(ys), np.max(ys)
#     x1, x2 = np.min(xs), np.max(xs)

#     w = x2 - x1
#     h = y2 - y1

#     cv2.rectangle(im, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)

# cv2.imwrite("tmp_im_bb.png", im)
