# Purpose: get two json file from one json file and multiple txts
import json

def load_txt_file(txt_file_path):
    with open(txt_file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    return set(lines)

def load_json_file(json_file_path):
    with open(json_file_path, 'r') as file:
        return json.load(file)

def save_json_file(json_dict, json_file_path):
    with open(json_file_path, 'w') as file:
        json.dump(json_dict, file)

def filter_images(json_dict, image_set):
    images = [image for image in json_dict['images'] if image['file_name'] in image_set]
    image_ids = {image['id'] for image in images}
    annotations = [annotation for annotation in json_dict['annotations'] if annotation['image_id'] in image_ids]
    return {'images': images, 'annotations': annotations, 'categories': json_dict['categories']}

def merge_jsons(json_dict1, json_dict2):
    id_map = {}
    next_id = len(json_dict1['images'])

    for image in json_dict2['images']:
        old_id = image['id']
        image['id'] = next_id
        id_map[old_id] = next_id
        next_id += 1

    for ann in json_dict2['annotations']:
        ann['image_id'] = id_map[ann['image_id']]

    merged_json = json_dict1.copy()
    merged_json['images'] += json_dict2['images']
    merged_json['annotations'] += json_dict2['annotations']
    merged_json['categories'] = json_dict1['categories']
    return merged_json

def main():
    # Load the existing JSON files
    day_json = load_json_file('/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/train_day.json')
    night_json = load_json_file('/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/train_night.json')

    # Load the image names from the txt files
    day_images = load_txt_file('/home/aghosh/Projects/2PCNet/Scripts/txt_out_train/day_image.txt')
    dawn_dusk_images = load_txt_file('/home/aghosh/Projects/2PCNet/Scripts/txt_out_train/dawn_dusk_images.txt')
    night_images = load_txt_file('/home/aghosh/Projects/2PCNet/Scripts/txt_out_train/night_images.txt')

    # Filter the images in the JSON files according to the txt files
    day_json_filtered = filter_images(day_json, day_images)
    dawn_dusk_json_filtered = filter_images(night_json, dawn_dusk_images)
    night_json_filtered = filter_images(night_json, night_images)

    # Merge the filtered JSON files
    day_dawn_dusk_json = merge_jsons(day_json_filtered, dawn_dusk_json_filtered)
    dawn_dusk_night_json = merge_jsons(dawn_dusk_json_filtered, night_json_filtered)

    # Save the merged JSON files
    save_json_file(day_dawn_dusk_json, 'train_day_dawn_dusk_cur.json')
    save_json_file(dawn_dusk_night_json, 'train_dawn_dusk_night_cur.json')

    # Print out the count of images and annotations in each merged JSON
    print(f"train_day_dawn_dusk_cur.json contains {len(day_dawn_dusk_json['images'])} images and {len(day_dawn_dusk_json['annotations'])} annotations")
    print(f"train_dawn_dusk_night_cur.json contains {len(dawn_dusk_night_json['images'])} images and {len(dawn_dusk_night_json['annotations'])} annotations")

if __name__ == '__main__':
    main()
