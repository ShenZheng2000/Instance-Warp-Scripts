
src_json = "/home/aghosh/Projects/2PCNet/Datasets/cityscapes/gt_detection/instancesonly_filtered_gtFine_train_poly_simple.json"

import json
import random
import matplotlib.pyplot as plt
import os
import shutil

# Purpose: Create a balanced subset of images from the Cityscapes dataset

COUNT = 250 # 250 for 25%
# COUNT = 500 # 500 for 50%

# Set the random seed for reproducibility
random.seed(0)

# Load the dictionary from the JSON file
src_json = "/home/aghosh/Projects/2PCNet/Datasets/cityscapes/gt_detection/instancesonly_filtered_gtFine_train_poly_simple.json"
with open(src_json, 'r') as json_file:
    data = json.load(json_file)

print("Total Images:", len(data))

# Define area thresholds for small, medium, and large bounding boxes
small_threshold = 32**2
medium_threshold = 96**2

def get_ratio():

    # Create a list to store ratios and corresponding image filenames
    ratios = []

    # Iterate through each image and its annotations
    for image_filename, annotations in data.items():
        small_count = 0
        medium_count = 0
        large_count = 0
        
        # Check if there are no annotations (empty list)
        if len(annotations) == 0:
            continue
        
        # Iterate through each annotation for the image
        for annotation in annotations:
            # Calculate the area of the bounding box
            bbox_area = (annotation[2] - annotation[0]) * (annotation[3] - annotation[1])
            
            # Count the bounding box based on area threshold
            if bbox_area <= small_threshold:
                small_count += 1
            elif bbox_area <= medium_threshold:
                medium_count += 1
            else:
                large_count += 1
        
        # Calculate the small:medium:large ratio
        total_count = small_count + medium_count + large_count
        ratio = (small_count / total_count, medium_count / total_count, large_count / total_count)
        
        # Add the ratio and image filename to the list
        ratios.append((image_filename, ratio))

    return ratios

def ratio_deviation(ratio):
    total = sum(ratio)

    if total == 0:
        return float('inf')

    # Calculate the absolute differences between each component of the ratio and 1/3
    deviation_small = (ratio[0] / total - 1/3)
    deviation_medium = (ratio[1] / total - 1/3)
    deviation_large = (ratio[2] / total - 1/3)

    # Calculate the average deviation
    average_deviation = (deviation_small + deviation_medium + deviation_large) / 3

    return average_deviation


def get_images():

    ratios = get_ratio()


    # Calculate deviation for each image
    deviations = [(image, ratio_deviation(ratio)) for image, ratio in ratios]

    # Sort by deviation
    sorted_by_deviation = sorted(deviations, key=lambda x: x[1])

    # Select the top N balanced images
    N_balanced = COUNT  # or any other number you prefer
    selected_balanced_images = [image for image, _ in sorted_by_deviation[:N_balanced]]

    # Identify and sort small-dominant and large-dominant images, excluding already selected balanced images
    small_dominant_images = []
    large_dominant_images = []

    for image, ratio in ratios:
        if image not in selected_balanced_images:
            if ratio[0] > ratio[1] and ratio[0] > ratio[2]:  # Small-dominant
                small_dominant_images.append((image, ratio[0]))
            elif ratio[2] > ratio[1] and ratio[2] > ratio[0]:  # Large-dominant
                large_dominant_images.append((image, ratio[2]))

    # Sort the small-dominant and large-dominant images based on their respective ratios
    small_dominant_images.sort(key=lambda x: x[1], reverse=True)  # Sort by small ratio
    large_dominant_images.sort(key=lambda x: x[1], reverse=True)  # Sort by large ratio

    # print("len(small_dominant_images) is", len(small_dominant_images))
    # print("len(large_dominant_images) is", len(large_dominant_images))

    # Optionally, limit the number of images from each set
    desired_count = COUNT  # adjust this as needed
    num_small_dominant = min(len(small_dominant_images), desired_count)
    num_large_dominant = min(len(large_dominant_images), desired_count)

    selected_small_dominant = [image for image, _ in small_dominant_images[:num_small_dominant]]
    selected_large_dominant = [image for image, _ in large_dominant_images[:num_large_dominant]]

    # Combine all sets
    final_selected_images = selected_balanced_images + selected_small_dominant + selected_large_dominant

    return final_selected_images


def check_ratio():
    final_selected_images = get_images()

    ###################### For the final set of images, calculate the small:medium:large ratio ######################
    # Initialize counts for each size category
    final_small_count = 0
    final_medium_count = 0
    final_large_count = 0

    # Calculate cumulative counts for the final set
    for image_filename in final_selected_images:
        # Assuming 'data' contains the annotations for each image
        annotations = data.get(image_filename, [])

        # Count the bounding boxes based on area threshold
        for annotation in annotations:
            bbox_area = (annotation[2] - annotation[0]) * (annotation[3] - annotation[1])
            if bbox_area <= small_threshold:
                final_small_count += 1
            elif bbox_area <= medium_threshold:
                final_medium_count += 1
            else:
                final_large_count += 1

    # Calculate the final small:medium:large ratio
    total_final_count = final_small_count + final_medium_count + final_large_count
    final_ratio = (
        final_small_count / total_final_count,
        final_medium_count / total_final_count,
        final_large_count / total_final_count,
    )

    print("Final Ratio (Small:Medium:Large):", final_ratio)
    print("Total Selected Images:", len(final_selected_images))



def copy_images_and_annotations(source_image_folder, source_annotation_folder, destination_image_folder, destination_annotation_folder, image_filenames_to_match):
    # Create a list of annotation filename patterns to match
    annotation_filename_patterns = [
        "gtFine_labelTrainIds.png",
        "gtFine_labelIds.png",
        "gtFine_color.png",
        "gtFine_instanceIds.png",
        # Add more annotation filename patterns as needed
    ]

    # Iterate through the source image folder and its subdirectories
    for root, _, files in os.walk(source_image_folder):
        for file in files:
            if file in image_filenames_to_match:
                # Construct the source and destination paths for images
                source_image_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_image_path, source_image_folder)
                destination_image_path = os.path.join(destination_image_folder, relative_path)

                # Create the destination directory if it doesn't exist
                os.makedirs(os.path.dirname(destination_image_path), exist_ok=True)

                # Copy the matched image to the destination image folder while maintaining the subfolder structure
                shutil.copy(source_image_path, destination_image_path)

                # Iterate through annotation filename patterns and copy matching annotations
                for pattern in annotation_filename_patterns:

                    source_annotation_path = os.path.join(source_annotation_folder, relative_path.replace("leftImg8bit.png", pattern))
                    # print("source_annotation_path", source_annotation_path)
                    destination_annotation_path = os.path.join(destination_annotation_folder, relative_path.replace("leftImg8bit.png", pattern))

                    # Create the destination directory if it doesn't exist
                    os.makedirs(os.path.dirname(destination_annotation_path), exist_ok=True)

                    # Copy the matched annotation to the destination annotation folder while maintaining the subfolder structure
                    shutil.copy(source_annotation_path, destination_annotation_path)



# Example usage:
source_image_folder = '/home/aghosh/Projects/2PCNet/Datasets/cityscapes/leftImg8bit/train'
source_annotation_folder = '/home/aghosh/Projects/2PCNet/Datasets/cityscapes/gtFine/train'

destination_image_folder = f"{source_image_folder}_uniform_{int(COUNT/10)}"
destination_annotation_folder = f"{source_annotation_folder}_uniform_{int(COUNT/10)}"

# print("destination_image_folder", destination_image_folder)
# print("destination_annotation_folder", destination_annotation_folder)
# exit()

os.makedirs(destination_image_folder, exist_ok=True)
os.makedirs(destination_annotation_folder, exist_ok=True)

image_filenames_to_match = get_images()
check_ratio()
# print("len(image_filenames_to_match)", len(image_filenames_to_match))

copy_images_and_annotations(source_image_folder, source_annotation_folder, destination_image_folder, destination_annotation_folder, image_filenames_to_match)
