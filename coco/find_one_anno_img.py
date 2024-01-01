import json

def filter_images_with_large_objects(json_file, min_area):
    # Load the COCO format JSON file
    with open(json_file, 'r') as f:
        coco_data = json.load(f)

    # Create a dictionary to store image IDs and their corresponding annotation areas
    image_annotation_areas = {}

    # Iterate through annotations and calculate the total area for each image
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        area = annotation['area']
        if image_id in image_annotation_areas:
            image_annotation_areas[image_id] += area
        else:
            image_annotation_areas[image_id] = area

    # Create a list to store image IDs with objects larger than min_area
    images_with_large_objects = []

    # Iterate through images and check the total annotation area
    for image in coco_data['images']:
        image_id = image['id']
        if image_id in image_annotation_areas and image_annotation_areas[image_id] > min_area:
            images_with_large_objects.append(image)

    return images_with_large_objects

# Example usage:
json_file_path = '/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/train_rainy.json'
min_area_threshold = 7e5  # 400x400 = 160,000 pixels
images_with_large_objects = filter_images_with_large_objects(json_file_path, min_area_threshold)

# Print the list of images with large objects
for image in images_with_large_objects:
    print(f"Image ID: {image['id']} - File Name: {image['file_name']}")
