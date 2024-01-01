import json

src = '/home/aghosh/Projects/2PCNet/Methods/Night-Object-Detection/outputs/bdd100k_fovea_05x/inference/coco_instances_results.json'

# Load JSON data from a file
with open(src, 'r') as json_file:
    data = json.load(json_file)

# Initialize variables to store min and max values
min_x, min_y, max_width, max_height = float('inf'), float('inf'), float('-inf'), float('-inf')

# Iterate through the data and find min and max values
for item in data:
    bbox = item["bbox"]
    min_x = min(min_x, bbox[0])
    min_y = min(min_y, bbox[1])
    max_width = max(max_width, bbox[2])
    max_height = max(max_height, bbox[3])

# Print the results
print("Minimum x:", min_x)
print("Minimum y:", min_y)
print("Maximum width:", max_width)
print("Maximum height:", max_height)
