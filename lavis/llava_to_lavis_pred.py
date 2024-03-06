import json
import os

# TODO: modify this code later, and include into readme

# llava = "/longdata/anurag_storage/workzone_gem/captions_llava/captions_llava_val_gps_split_results.json"
# lavis = "/longdata/anurag_storage/workzone_gem/captions_lavis/captions_lavis_val_gps_split_results_lavis.json"

llava = "/longdata/anurag_storage/workzone_gem/captions_llava/captions_llava_val_gps_split_results_pretrained.json"
lavis = "/longdata/anurag_storage/workzone_gem/captions_lavis/captions_lavis_val_gps_split_results_lavis_pretrained.json"

# Read data from the JSON file
with open(llava, 'r') as file:
    data = json.load(file)

# Append new key-value pairs
for i, d in enumerate(data, start=1):
    d["image_id"] = i

# Ensure the directory for the output file exists
os.makedirs(os.path.dirname(lavis), exist_ok=True)

# Save the modified data back to a JSON file
with open(lavis, 'w') as file:
    json.dump(data, file, indent=4)
