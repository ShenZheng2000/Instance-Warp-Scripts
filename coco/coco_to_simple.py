# Purpose: extract bboxes from coco jsons

import json

# Function to convert COCO bbox format to [x1, y1, x2, y2] format
def convert_bbox(coco_bbox):
    x_min, y_min, width, height = coco_bbox
    x2 = x_min + width
    y2 = y_min + height
    return [x_min, y_min, x2, y2]

# Assuming `coco_data` is your loaded COCO format data
# Replace 'your_coco_file.json' with the path to your COCO JSON file
with open('/home/aghosh/Projects/2PCNet/Datasets/acdc/gt_detection/train.json', 'r') as f:
    coco_data = json.load(f)

# Extracting images' file names and IDs for reference
image_id_to_file_name = {image['id']: image['file_name'] for image in coco_data['images']}

# Preparing the new data structure based on your format
extracted_bboxes = {}

for annotation in coco_data['annotations']:
    image_id = annotation['image_id']
    coco_bbox = annotation['bbox']
    converted_bbox = convert_bbox(coco_bbox)
    
    # Get the corresponding image file name
    image_file_name = image_id_to_file_name[image_id]
    
    # Initialize the list if this is the first bbox for this image
    if image_file_name not in extracted_bboxes:
        extracted_bboxes[image_file_name] = []
    
    # Append the converted bbox
    extracted_bboxes[image_file_name].append(converted_bbox)

# Save the new JSON file with extracted bounding boxes
with open('/home/aghosh/Projects/2PCNet/Datasets/acdc/gt_detection/train_simple.json', 'w') as f:
    json.dump(extracted_bboxes, f, indent=4)

print("Extraction and save completed.")
