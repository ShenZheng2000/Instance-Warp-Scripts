import json

# Load the JSON file
with open('/home/aghosh/Projects/2PCNet/Datasets/cityscapes_seg2det.json', 'r') as json_file:
    data = json.load(json_file)

# Initialize variables to keep track of any issues
images_without_boxes = []
empty_boxes = []

# Iterate through the JSON data
for image_path, bounding_boxes in data.items():
    if not bounding_boxes:
        # If the bounding boxes list is empty, add the image path to the empty_boxes list
        empty_boxes.append(image_path)
    elif all(not bbox for bbox in bounding_boxes):
        # If all bounding boxes for an image are empty, add the image path to the empty_boxes list
        empty_boxes.append(image_path)
    elif len(bounding_boxes) == 1 and not any(bounding_boxes[0]):
        # If there is only one bounding box for an image, and it's empty, add the image path to the empty_boxes list
        empty_boxes.append(image_path)
    elif len(bounding_boxes) == 1 and all(not any(bbox) for bbox in bounding_boxes):
        # If there is only one bounding box for an image, and it's empty, add the image path to the empty_boxes list
        empty_boxes.append(image_path)
    elif len(bounding_boxes) > 1 and all(not bbox for bbox in bounding_boxes):
        # If all bounding boxes for an image are empty, add the image path to the empty_boxes list
        empty_boxes.append(image_path)

    if not bounding_boxes:
        # If there are no bounding boxes for an image, add the image path to the images_without_boxes list
        images_without_boxes.append(image_path)

# Check and print the results
if empty_boxes:
    print("Images with empty or no bounding boxes:")
    for image_path in empty_boxes:
        print(image_path)
else:
    print("All images have valid bounding boxes.")

if images_without_boxes:
    print("\nImages without bounding boxes:")
    for image_path in images_without_boxes:
        print(image_path)
else:
    print("All images have associated bounding boxes.")


# Images with empty or no bounding boxes:
# strasbourg/strasbourg_000000_036016_leftImg8bit.png

# Images without bounding boxes:
# strasbourg/strasbourg_000000_036016_leftImg8bit.png
