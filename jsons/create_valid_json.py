import json
import os

# Purpose: Create an json file with ONLY valid vanishing points

dataset_path = "/home/aghosh/Projects/2PCNet/Datasets"
# base_name = "train_day"
# task_name = "val_night"
# task_name = "train_night"
task_name = 'train_clear'

def get_invalid_vanishing_points(data, image_width, image_height):
    invalid_files = []

    print(f"total vps {len(data.keys())}")

    for file_name, vanishing_point in data.items():
        x, y = vanishing_point
        # Check if both coordinates are out of bounds
        if not (0 <= x < image_width) and not (0 <= y < image_height):
            invalid_files.append(os.path.basename(file_name))
        
    return invalid_files

def main():
    file_path = f"/home/aghosh/Projects/2PCNet/Datasets/VP/bdd100k_all_vp.json" # NOTE: specficiy train or val
    image_width = 1280 
    image_height = 720

    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    # Get invalid vanishing points
    invalid_files = get_invalid_vanishing_points(data, image_width, image_height)

    print("Number of invalid vanishing points:", len(invalid_files))

    # Load COCO json file
    coco_path = f"{dataset_path}/bdd100k/coco_labels/{task_name}.json"
    # coco_path = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/train_clear.json" # NOTE: keep this fixed
    with open(coco_path, 'r') as f:
        coco_data = json.load(f)
        
    print(f"total images {len(coco_data['images'])}")


    # Filter images
    filtered_images = []
    count_filtered = 0
    names_not_found = []

    for img in coco_data['images']:
        base_name = os.path.basename(img['file_name'])
        if base_name not in invalid_files:
            filtered_images.append(img)
        else:
            count_filtered += 1
            print("Filtered out:", base_name)
    print("Number of images filtered:", count_filtered)


    # Names not found in COCO dataset => OK for now
    for name in invalid_files:
        if name not in [os.path.basename(img['file_name']) for img in coco_data['images']]:
            names_not_found.append(name)    
    print("Names not found in COCO dataset:", names_not_found)


    # Replace images in COCO data
    coco_data['images'] = filtered_images


    # Save the filtered COCO json file
    with open(f'{dataset_path}/bdd100k/coco_labels/{task_name}_valid_vp.json', 'w') as f:
        json.dump(coco_data, f)

if __name__ == "__main__":
    main()
