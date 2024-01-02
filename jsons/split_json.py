# Purpose: split one json file into multiple json files based on give txt files
import json

# Function to read image names from a text file into a set
def read_image_names(file_path):
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file)

# Create two sets of image names
dawn_dusk_image_set = read_image_names('txt_out_train/dawn_dusk_images.txt')
night_image_set = read_image_names('txt_out_train/night_images.txt')

# Load COCO JSON file
with open('/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/train_night.json') as f:
    coco = json.load(f)

# Filter images
dawn_dusk_images = [image for image in coco['images'] if image['file_name'] in dawn_dusk_image_set]
night_images = [image for image in coco['images'] if image['file_name'] in night_image_set]

# Get image IDs for further filtering of annotations
dawn_dusk_image_ids = {image['id'] for image in dawn_dusk_images}
night_image_ids = {image['id'] for image in night_images}

# Filter annotations
dawn_dusk_annotations = [annotation for annotation in coco['annotations'] if annotation['image_id'] in dawn_dusk_image_ids]
night_annotations = [annotation for annotation in coco['annotations'] if annotation['image_id'] in night_image_ids]

# Create new COCO JSONs
dawn_dusk_coco = {**coco, 'images': dawn_dusk_images, 'annotations': dawn_dusk_annotations}
night_coco = {**coco, 'images': night_images, 'annotations': night_annotations}

# Save new COCO JSONs
with open('train_dawn_dusk_cur.json', 'w') as f:
    json.dump(dawn_dusk_coco, f)

with open('train_night_cur.json', 'w') as f:
    json.dump(night_coco, f)

# Print out the number of images and annotations
print(f"Dawn/Dusk: {len(dawn_dusk_images)} images, {len(dawn_dusk_annotations)} annotations")
print(f"Night: {len(night_images)} images, {len(night_annotations)} annotations")