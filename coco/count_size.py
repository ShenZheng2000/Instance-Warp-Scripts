
import json

def calculate_object_sizes_percentage(coco_json):
    small, medium, large = 0, 0, 0

    # Iterate through each annotation to calculate the area and categorize
    for annotation in coco_json['annotations']:
        x1, y1, w, h = annotation['bbox']
        area = w * h

        # Categorize based on area
        if area < 32**2:
            small += 1
        elif area <= 96**2:
            medium += 1
        else:
            large += 1

    # Total number of objects
    total_objects = small + medium + large

    # Calculate percentages
    small_percentage = (small / total_objects) * 100 if total_objects else 0
    medium_percentage = (medium / total_objects) * 100 if total_objects else 0
    large_percentage = (large / total_objects) * 100 if total_objects else 0

    return small_percentage, medium_percentage, large_percentage

# Example usage
with open("/home/aghosh/Projects/2PCNet/Datasets/Argoverse/Argoverse-HD/coco_labels/val.json", 'r') as file:
    coco_json = json.load(file)

small_percentage, medium_percentage, large_percentage = calculate_object_sizes_percentage(coco_json)
print(f"Small: {small_percentage:.2f}%, Medium: {medium_percentage:.2f}%, Large: {large_percentage:.2f}%")

# compute res = [(small/medium) + (medium/large)]
res = (small_percentage/medium_percentage) + (medium_percentage/large_percentage)
print(f"Res: {res:.2f}")
