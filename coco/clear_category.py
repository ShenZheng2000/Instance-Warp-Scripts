import json
import sys

src = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels"
task = sys.argv[1]

# Specify the path to your input and output JSON files
input_json_path = f'{src}/bdd100k_labels_images_{task}_ori.json'
output_json_path = f'{src}/bdd100k_labels_images_{task}.json'

# List of category names to keep
categories_to_keep = ["person", # yes
                        "bicycle", # yes
                        "car",  # yes
                        "motorcycle",  # yes
                        "bus",   # yes
                        "train",   # yes
                        "truck",  # yes
                        "traffic light",   # yes
                        "stop sign"  # yes
                        ]

# Read the input JSON file
with open(input_json_path, 'r') as input_json_file:
    coco_data = json.load(input_json_file)

# Filter categories and keep only those in 'categories_to_keep'
filtered_categories = [category for category in coco_data['categories'] \
                       if category['name'] in categories_to_keep]

# Update the 'categories' field in the COCO data
coco_data['categories'] = filtered_categories

# Write the filtered data to the output JSON file
with open(output_json_path, 'w') as output_json_file:
    json.dump(coco_data, output_json_file, indent=4)

print(f"Filtered data saved to {output_json_path}")
