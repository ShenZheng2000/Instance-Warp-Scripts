import json
import cv2
import os

# Purpose: Visualize the annotations in the COCO format JSON file

# Path to COCO format JSON file
# json_file_path = '/longdata/anurag_storage/DENSE/Scripts/coco_annotations.json'
# json_file_path = '/longdata/anurag_storage/DENSE/Scripts/output_jsons/val_dense_fog.json'
# json_file_path = '/longdata/anurag_storage/DENSE/Scripts/output_jsons/train_dense_fog.json'
# json_file_path = '/longdata/anurag_storage/DENSE/Scripts/output_jsons/train_snow.json'
json_file_path = '/longdata/anurag_storage/DENSE/Scripts/output_jsons/val_snow.json'

# Path to the folder containing images
image_folder = '/longdata/anurag_storage/DENSE/cam_stereo_left_lut'

# Number of images to process (set your desired limit)
image_limit = 10

# Output folder to save images with bounding boxes and labels
output_folder = 'output_folder'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the COCO JSON file
with open(json_file_path, 'r') as json_file:
    coco_data = json.load(json_file)

# Get the list of images
images = coco_data['images'][:image_limit]

# Iterate through the images
for image_info in images:
    image_id = image_info['id']
    image_filename = image_info['file_name']

    # Load the image
    image_path = os.path.join(image_folder, image_filename)
    image = cv2.imread(image_path)

    # Get the annotations for the current image
    annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] == image_id]

    # Draw bounding boxes and labels
    for annotation in annotations:
        category_id = annotation['category_id']
        category_info = next(cat for cat in coco_data['categories'] if cat['id'] == category_id)
        category_name = category_info['name']
        bbox = annotation['bbox']
        bbox = [int(coord) for coord in bbox]

        # Draw the bounding box
        color = (0, 255, 0)  # Green color
        thickness = 2
        cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), color, thickness)

        # Add label text
        label = f"{category_name}"
        label_position = (bbox[0], bbox[1] - 10)  # Position just above the bounding box
        cv2.putText(image, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)

    # Save the image with bounding boxes and labels
    output_path = os.path.join(output_folder, image_filename)
    cv2.imwrite(output_path, image)

print(f"Images with bounding boxes and labels saved to {output_folder}")
