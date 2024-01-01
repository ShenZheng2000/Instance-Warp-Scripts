import json
import os

import json
import os

# Paths to source JSON files
src_jsons = [
    "/home/aghosh/Projects/2PCNet/Datasets/VP/dark_zurich_all_vp.json",
    "/home/aghosh/Projects/2PCNet/Datasets/VP/cityscapes_all_vp.json",
    "/home/aghosh/Projects/2PCNet/Datasets/VP/acdc_all_vp.json",
    "/home/aghosh/Projects/2PCNet/Datasets/VP/synthia_all_vp.json"
]
tgt_json = "/home/aghosh/Projects/2PCNet/Datasets/VP/cs_dz_acdc_synthia_all_vp.json"

merged_data = {}
image_count = {}
all_basenames = set()

# Loop over each source JSON and merge its content
for src_json in src_jsons:
    with open(src_json, 'r') as file:
        data = json.load(file)
    
    # Store the number of images for the current JSON
    image_count[src_json] = len(data)

    # Extract basenames from the keys in the current JSON
    current_basenames = {os.path.basename(key) for key in data.keys()}
    all_basenames.update(current_basenames)
    
    # Merge the current dictionary into the main one
    merged_data.update(data)

# Count the number of common basenames among all JSONs
common_basename_count = len(all_basenames)

# Write the merged data to the target JSON file
with open(tgt_json, 'w') as merged_file:
    json.dump(merged_data, merged_file, indent=4)

print(f"Merged JSON file created as {tgt_json}")
print(f"Number of common basenames: {common_basename_count}")
for src, count in image_count.items():
    print(f"Number of images in {src}: {count}")