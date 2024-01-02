import cv2
import numpy as np
import os
import glob
import json
import sys

# NOTE: for synthia images, preconvert gray to color using this script: /home/aghosh/Projects/2PCNet/Scripts/sem_seg/gray_to_color.py
# NOTE: for synthia gt, use get_seg_tmp.py!!!!!

'''
The expected structure in json file
{
"path/to/image1.png": 
    [
    [x1, y1, x2, y2], # bbox1
    ...
    ],
"path/to/image2.png": 
    ...
}
'''

def get_classes():
    return cityscapes_classes()

def get_palette():
    return cityscapes_palette()

def get_foreground_classes():
    return get_cityscape_foreground_classes()


def cityscapes_classes():
    return [
        'road', 'sidewalk', 'building', 
        'wall', 'fence', 'pole',
        'traffic light', 'traffic sign', 'vegetation', 
        'terrain', 'sky',
        'person', 'rider', 'car', 
        'truck', 'bus', 'train', 
        'motorcycle', 'bicycle'
    ]

def cityscapes_palette(): # rgb colors
    return [
            [128, 64, 128], [244, 35, 232], [70, 70, 70], 
            [102, 102, 156],[190, 153, 153], [153, 153, 153], 
            [250, 170, 30], [220, 220, 0], [107, 142, 35], 
            [152, 251, 152], [70, 130, 180],
            [220, 20, 60],[255, 0, 0], [0, 0, 142], 
            [0, 0, 70], [0, 60, 100], [0, 80, 100], 
            [0, 0, 230], [119, 11, 32]
            ]


def get_cityscape_foreground_classes():
    # Define foreground classes based on your understanding or domain knowledge
    return [
            'traffic light', 'traffic sign', 
            'person', 'rider', 'car', 
            'truck', 'bus', 'train', 
            'motorcycle', 'bicycle', 
            ]

def convert_to_bgr(palette):
    return [color[::-1] for color in palette]

def visualize_bboxes(image, bboxes):
    for bbox in bboxes:
        cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
    return image


def int64_to_int(data):
    if isinstance(data, list):
        return [int64_to_int(item) for item in data]
    elif isinstance(data, dict):
        return {key: int64_to_int(value) for key, value in data.items()}
    elif isinstance(data, (np.int64, np.int32)):
        return int(data)
    else:
        return data

def extract_bboxes(seg_map, foreground_classes, classes, palette):
    '''
    Extract bounding boxes from a segmentation map.
    '''
    bboxes = []

    for idx, cls in enumerate(classes):
        if cls in foreground_classes:
            # Create a binary mask for the current class
            mask = np.all(seg_map == palette[idx], axis=-1)

            # Label each connected component (or instance) in the mask
            num_labels, labels_im = cv2.connectedComponents(mask.astype(np.uint8))

            for label in range(1, num_labels):  # Start from 1 to ignore background
                rows, cols = np.nonzero(labels_im == label)
                if len(rows) == 0:  # Skip empty labels
                    continue

                x_min, x_max = cols.min(), cols.max()
                y_min, y_max = rows.min(), rows.max()
                bboxes.append([x_min, y_min, x_max, y_max])

    return bboxes

def main(img_folder, seg_folder, output_json, 
         vis_flag=False, 
         dataset_name="cityscapes", 
         debug_count=1e5):
    # Create an empty dictionary to store bounding boxes
    bboxes_dict = {}

    # Use the ** wildcard to search for images recursively
    img_files = glob.glob(os.path.join(img_folder, '**/*.png'), recursive=True)

    count = 0

    for img_path in img_files:
        # Get the relative path of the image within img_folder
        relative_img_path = os.path.relpath(img_path, img_folder)

        # Build the corresponding path in the segmentation folder
        seg_path = os.path.join(seg_folder, relative_img_path)

        # Replace image file extension with "_gtFine_color.png" for segmentation map
        if dataset_name == 'gta':
            seg_path = seg_path

        elif dataset_name == 'synthia':
            seg_path = seg_path.replace(".png", "_labelTrainIds.png")

        elif dataset_name == 'cityscapes':
            seg_path = seg_path.replace("_leftImg8bit.png", "_gtFine_color.png")

        elif dataset_name == 'IDD':
            seg_path = seg_path.replace("_leftImg8bit.png", "_gtFine_labelColors.png")
        
        # Check if the segmentation file exists
        if os.path.exists(seg_path):

            # Read the image and segmentation map
            original_image = cv2.imread(img_path)
            seg_map = cv2.imread(seg_path)

            # Extract the bounding boxes based on dataset name
            foreground_classes = get_foreground_classes()
            bgr_palette = convert_to_bgr(get_palette())
            bboxes = extract_bboxes(seg_map, foreground_classes, get_classes(), bgr_palette)

            # convert int64 to int
            bboxes = int64_to_int(bboxes)

            # Store bounding boxes in the dictionary
            bboxes_dict[relative_img_path] = bboxes


            if vis_flag:
                result_image = visualize_bboxes(original_image, bboxes)
                result_image_path = os.path.join(dataset_name, f"result_{relative_img_path}")

                os.makedirs(os.path.dirname(result_image_path), exist_ok=True)

                cv2.imwrite(result_image_path, result_image)

                if count == debug_count:
                    break

            count += 1

            if count % 50 == 0:
                print(f"finished {count} images")


    # Save the bounding boxes dictionary as a JSON file
    if not vis_flag:
        with open(output_json, 'w') as json_file:
            # print("bboxes_dict is", bboxes_dict)
            json.dump(bboxes_dict, json_file)


if __name__ == '__main__':

    src_dir = "/home/aghosh/Projects/2PCNet/Datasets"
    dataset_name = sys.argv[1] # ['gta', 'synthia', 'cityscapes', 'IDD']
    vis_flag = False

    # NOTE: this is for gta dataset
    if dataset_name == 'gta':
        img_folder = os.path.join(src_dir, f"{dataset_name}/images")
        seg_folder = os.path.join(src_dir, f"{dataset_name}/labels")
    elif dataset_name == 'synthia':
        img_folder = os.path.join(src_dir, f"{dataset_name}/RGB")
        seg_folder = os.path.join(src_dir, f"{dataset_name}/GT/LABELS_CONVERT")
    elif dataset_name == 'cityscapes':
        img_folder = os.path.join(src_dir, f"{dataset_name}/leftImg8bit/train")
        seg_folder = os.path.join(src_dir, f"{dataset_name}/gtFine/train")
    elif dataset_name == 'IDD':
        img_folder = os.path.join(src_dir, f"{dataset_name}/IDD_Segmentation/leftImg8bit/train")
        seg_folder = os.path.join(src_dir, f"{dataset_name}/IDD_Segmentation/gtFine/train")

    output_json = os.path.join(src_dir, f"{dataset_name}_seg2det.json")

    # debug_count = 1e5

    os.makedirs(dataset_name, exist_ok=True)

    main(img_folder, 
         seg_folder, 
         output_json, 
         vis_flag=vis_flag, 
         dataset_name=dataset_name,
         debug_count=10,
         )