import json

# Load the COCO format JSON file
with open('/home/aghosh/Projects/2PCNet/Datasets/dense/coco_labels/val_dense_fog.json', 'r') as json_file:
    coco_data = json.load(json_file)

# Count the number of images
num_images = len(coco_data['images'])

print(f'Total number of images: {num_images}')
