import json
import random
import os
import sys

# NOTE: split with train/test = 4:1, and train/test in different days. 

# set seed for reproducibility
random.seed(0)

weather = sys.argv[1] # ['dense_fog', 'snow']

# Paths to COCO JSON file, list of image basenames, and output folders
coco_json_path = '/longdata/anurag_storage/DENSE/Scripts/coco_annotations.json'
image_basenames_folder  = '/longdata/anurag_storage/DENSE/SeeingThroughFog/splits'
output_folder = '/home/aghosh/Projects/2PCNet/Datasets/dense/coco_labels'
specific_txt_files = [f'{weather}_day.txt', f'{weather}_night.txt'] 

os.makedirs(output_folder, exist_ok=True)

# Initialize an empty list to collect modified image basenames
modified_image_basenames = []

# Iterate through the specific text files
for filename in specific_txt_files:
    file_path = os.path.join(image_basenames_folder, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                # Extract the date part, replace comma with underscore, and add .png extension
                modified_basename = line.strip().replace(',', '_') + '.png'
                modified_image_basenames.append(modified_basename)

# # Print the first modified basename for verification
# print("First modified image basename:", modified_image_basenames[0])
# exit()

# Load the COCO JSON file
with open(coco_json_path, 'r') as json_file:
    coco_data = json.load(json_file)

# Group images by day
image_groups = {}
for basename in modified_image_basenames:
    day = basename.split('_')[0]  # Correctly extract the date
    if day not in image_groups:
        image_groups[day] = []
    image_groups[day].append(basename)

# List of all days
all_days = list(image_groups.keys())

# Shuffle the list of days
random.shuffle(all_days)

# Calculate the number of days for training
total_days = len(all_days)
train_ratio = 0.8
num_train_days = int(total_days * train_ratio)

# Split the days into training and validation sets
train_days = all_days[:num_train_days]
val_days = all_days[num_train_days:]

# Collect train and validation image basenames
train_images = [img for day in train_days for img in image_groups[day]]
val_images = [img for day in val_days for img in image_groups[day]]

# NOTE: Separate validation images into day and night
# Function to modify basenames as per your existing code
def modify_basename(basename):
    return basename.strip().replace(',', '_') + '.png'

# Read and modify basenames from day and night text files
day_basenames = set(modify_basename(line) for line in open(os.path.join(image_basenames_folder, f'{weather}_day.txt')))
night_basenames = set(modify_basename(line) for line in open(os.path.join(image_basenames_folder, f'{weather}_night.txt')))

# Separate validation images into day and night
val_images_day = [img for img in val_images if img in day_basenames]
val_images_night = [img for img in val_images if img in night_basenames]

# Separate training images into day and night
train_images_day = [img for img in train_images if img in day_basenames]
train_images_night = [img for img in train_images if img in night_basenames]

print("len(train_images)", len(train_images))
print("len(train_images_day)", len(train_images_day))
print("len(train_images_night)", len(train_images_night))

print("val_images", val_images)

print("len(val_images)", len(val_images))
print("len(val_images_day)", len(val_images_day))
print("len(val_images_night)", len(val_images_night))
exit()

# Convert val_images_day and val_images_night to their corresponding image IDs
val_image_ids_day = {image_id_map[img] for img in val_images_day if img in image_id_map}
val_image_ids_night = {image_id_map[img] for img in val_images_night if img in image_id_map}

# Filter COCO annotations for day and night based on image IDs
val_annotations_day = [ann for ann in coco_data['annotations'] if ann['image_id'] in val_image_ids_day]
val_annotations_night = [ann for ann in coco_data['annotations'] if ann['image_id'] in val_image_ids_night]

# # print the length of train and validation image basenames
# print("Number of training images:", len(train_images))
# print("Number of validation images:", len(val_images))

# # print the first 10 training and validation image basenames
# print("First 10 training image basenames:", train_images[:10])
# print("First 10 validation image basenames:", val_images[:10])
# exit()

# Create a mapping from image file names to image IDs
image_id_map = {img['file_name']: img['id'] for img in coco_data['images']}

# Convert train_images and val_images to their corresponding image IDs
train_image_ids = {image_id_map[img] for img in train_images if img in image_id_map}
val_image_ids = {image_id_map[img] for img in val_images if img in image_id_map}

# Filter COCO annotations based on image IDs
train_annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] in train_image_ids]
val_annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] in val_image_ids]

# print("train_annotations length", len(train_annotations))
# print("val_annotations length", len(val_annotations))
# exit()

# Create train and val JSON data
train_data = {
    "images": [img for img in coco_data['images'] if img['file_name'] in train_images],
    "annotations": train_annotations,
    "categories": coco_data['categories']
}

val_data = {
    "images": [img for img in coco_data['images'] if img['file_name'] in val_images],
    "annotations": val_annotations,
    "categories": coco_data['categories']
}

# Create val JSON data for day and night
val_data_day = {
    "images": [img for img in coco_data['images'] if img['file_name'] in val_images_day],
    "annotations": val_annotations_day,
    "categories": coco_data['categories']
}

val_data_night = {
    "images": [img for img in coco_data['images'] if img['file_name'] in val_images_night],
    "annotations": val_annotations_night,
    "categories": coco_data['categories']
}

# Output paths for train and val JSON files
train_json_path = os.path.join(output_folder, f'train_{weather}.json')
val_json_path = os.path.join(output_folder, f'val_{weather}.json')

# Output paths for val JSON files for day and night
val_json_path_day = os.path.join(output_folder, f'val_{weather}_day.json')
val_json_path_night = os.path.join(output_folder, f'val_{weather}_night.json')

# TODO: skip this for now, once debug is done, uncomment this
# # Write train and val JSON files
# with open(train_json_path, 'w') as train_file:
#     json.dump(train_data, train_file)

# with open(val_json_path, 'w') as val_file:
#     json.dump(val_data, val_file)

# Write val JSON files for day and night
with open(val_json_path_day, 'w') as val_file_day:
    json.dump(val_data_day, val_file_day)

with open(val_json_path_night, 'w') as val_file_night:
    json.dump(val_data_night, val_file_night)