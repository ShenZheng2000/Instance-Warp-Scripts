import json
from collections import defaultdict

def print_dict_in_table(dictionary, title):
    print(f"{title} Occurrences")
    print("-" * (len(title) + 11))
    for key, count in sorted(dictionary.items()):
        print(f"{key}: {count}")
    print()  # Add an extra newline for better separation

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def count_width_height_occurrences(file_path):
    # Load the JSON file
    coco_data = load_json(file_path)

    # Initialize dictionaries to count occurrences
    width_counts = defaultdict(int)
    height_counts = defaultdict(int)

    # Iterate over each image
    for image in coco_data["images"]:
        width = image["width"]
        height = image["height"]

        # Increment count for this width and height
        width_counts[width] += 1
        height_counts[height] += 1

    # Get the total number of images
    total_images = len(coco_data["images"])

    return width_counts, height_counts, total_images

# Example usage
file_path = '/home/aghosh/Projects/2PCNet/Datasets/data/annotations/geographic_da/instances_all.json'
width_counts, height_counts, total_images = count_width_height_occurrences(file_path)

# Print results in a table-like format
print("Total number of images:", total_images)
print()
print_dict_in_table(width_counts, "Width")
print_dict_in_table(height_counts, "Height")
