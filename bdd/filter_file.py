import json
import sys

# Purpose: filter coco json based on txt files
# Parameters:
    # coco_file (str): The path to the COCO formatted json file to be filtered.
    # filenames_txt (str): The path to the text file containing the list of filenames to be used for filtering.
    # output_file (str): The path to the output COCO formatted json file.
# Commands:
    # python filter_file.py $split $weather

def filter_coco_by_filenames(coco_file, filenames_txt, output_file):
    # 1. Load the filenames from the txt file
    with open(filenames_txt, 'r') as f:
        filenames = set(line.strip() for line in f.readlines())

    # 2. Load the COCO formatted json data
    with open(coco_file, 'r') as f:
        coco_data = json.load(f)

    # Filter images
    filtered_images = [img for img in coco_data['images'] if img['file_name'] in filenames]

    # Get the ids of the filtered images
    filtered_image_ids = set(img['id'] for img in filtered_images)

    # Filter annotations based on the image ids
    filtered_annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] in filtered_image_ids]

    # Update the COCO data to only contain the filtered images and annotations
    coco_data['images'] = filtered_images
    coco_data['annotations'] = filtered_annotations

    # 3. Save the filtered COCO data to a new json file
    with open(output_file, 'w') as f:
        json.dump(coco_data, f, indent=4)

    print("successfully dumped to", output_file)

if __name__ == '__main__':
    # TODO: change weather and get new output_coco_file!
    # clear.txt => rainy.txt
    # split = 'val'
    split = sys.argv[1]
    weather = sys.argv[2]
    # weather = 'daytime_good_weather'
    # weather = 'daytime_bad_weather'
    # weather = "clear_night"
    # weather = 'rainy_day'
    # weather = 'rainy_night'
    # weather = 'rainy_100'
    input_coco_file = f'/home/aghosh/Projects/2PCNet/Datasets/bdd100k_ori/labels/det_20/det_{split}_coco.json'
    input_txt_file = f'/home/aghosh/Projects/2PCNet/Scripts/bdd/{split}/{weather}.txt'
    output_coco_file = f'/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/{split}_{weather}.json'

    filter_coco_by_filenames(input_coco_file, input_txt_file, output_coco_file)