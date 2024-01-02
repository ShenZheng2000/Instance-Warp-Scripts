import json

# Purpose: explore the structure of a JSON file

# src_file = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k_ori/labels/det_20/det_val_coco.json"
# src_file = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_night.json"
src_file = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_day.json"

def explore_keys(data, prefix=""):
    if isinstance(data, dict):
        for key in data:
            if key == "type":
                print(prefix + key, ":", data[key])
            elif key == "categories" and isinstance(data[key], list):
                print(prefix + key, ":", data[key])
            else:
                print(prefix + key, ":")
            explore_keys(data[key], prefix + key + " -> ")
    elif isinstance(data, list) and data:
        # Only explore the first item in the list for brevity
        explore_keys(data[0], prefix + "[0] -> ")

# Load the JSON file
with open(src_file, 'r') as f:
    coco_data = json.load(f)

explore_keys(coco_data)