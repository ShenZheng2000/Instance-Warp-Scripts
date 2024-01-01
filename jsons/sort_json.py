import json
import os

# Step 1: Read the txt file
with open("/home/aghosh/Projects/2PCNet/Scripts/bdd/train/clear.txt", "r") as txt_file:
    filenames = [line.strip() for line in txt_file]

# Step 2: Read the JSON file
with open("/home/aghosh/Projects/2PCNet/Datasets/VP/bdd100k_all_vp.json", "r") as json_file:
    data = json.load(json_file)

# Create a basename to full path mapping
basename_to_fullpath = {os.path.basename(key): key for key in data.keys()}

# Sort the JSON data according to the order in the txt file
ordered_data = {basename_to_fullpath[filename]: data[basename_to_fullpath[filename]] for filename in filenames if filename in basename_to_fullpath}

# Step 4: Save the new dictionary to a new JSON file
with open("/home/aghosh/Projects/2PCNet/Datasets/VP/train_clear.json", "w") as json_file:
    json.dump(ordered_data, json_file, indent=4)

print("JSON data has been ordered and saved to ordered_output.json!")