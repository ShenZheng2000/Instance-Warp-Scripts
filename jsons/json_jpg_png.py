# Purpose: replace all jpgs with png in a json file
import json

json_file = '/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/train_night_cur_png.json'

# Read the JSON file
with open(json_file, 'r') as f:
    data = json.load(f)

# Convert the JSON object to a string
data_str = json.dumps(data)

# Replace .jpg with .png
data_str = data_str.replace('.jpg', '.png')

# Convert the string back to a JSON object
data = json.loads(data_str)

# Write the modified JSON object back to the file
with open(json_file, 'w') as f:
    json.dump(data, f)