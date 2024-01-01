import json

# Function to calculate the area of the bounding box
def calculate_area(bbox):
    return bbox[2] * bbox[3]  # width * height

# Load the original COCO JSON file
with open('/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/train_clear_valid_vp.json') as f:
    data = json.load(f)

# Filter annotations
filtered_annotations = [anno for anno in data['annotations'] if calculate_area(anno['bbox']) < 1024]

# Update the 'annotations' field with the filtered annotations
data['annotations'] = filtered_annotations

# Filter out images without annotations
image_ids_with_annotations = set([anno['image_id'] for anno in filtered_annotations])
data['images'] = [img for img in data['images'] if img['id'] in image_ids_with_annotations]

# Write the updated COCO data to a new JSON file
with open('train_clear_small_valid_vp.json', 'w') as f:
    json.dump(data, f)