import json
import os
import sys

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def create_category_mapping():
    # Mapping from source to destination categories
    return {
        0: 1,  # person to pedestrian
        1: 8,  # bicycle to bicycle
        2: 3,  # car to car
        3: 7,  # motorcycle to motorcycle
        4: 5,  # bus to bus
        5: 4,  # truck to truck
        6: 9,  # traffic_light to traffic light
        7: 10  # stop_sign to traffic sign
    }

def update_source_categories(source_categories, dest_categories, mapping):
    updated_categories = []
    dest_id_to_name = {cat['id']: cat['name'] for cat in dest_categories}

    # Add all destination categories that have a mapping in the source categories
    for source_cat in source_categories:
        if source_cat['id'] in mapping:
            new_id = mapping[source_cat['id']]
            if new_id in dest_id_to_name:
                updated_categories.append({'id': new_id, 'name': dest_id_to_name[new_id]})

    # Add 'rider' and 'train' categories which are not present in the source categories
    updated_categories.append({'id': 2, 'name': 'rider'})
    updated_categories.append({'id': 6, 'name': 'train'})

    # Sort categories by id
    updated_categories = sorted(updated_categories, key=lambda x: x['id'])

    return updated_categories

def update_annotations(annotations, mapping):
    for ann in annotations:
        if ann['category_id'] in mapping:
            ann['category_id'] = mapping[ann['category_id']]
    return annotations

def rename_image_keys(images):
    for img in images:
        if 'name' in img:
            img['file_name'] = img.pop('name')
    return images

if __name__ == "__main__":
    # Load source and destination datasets
    source_data = load_json('/home/aghosh/Projects/2PCNet/Datasets/Argoverse/Argoverse-HD/annotations/train.json')
    dest_data = load_json('/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_rainy_100.json')

    category_mapping = create_category_mapping()

    # Update categories in the source data based on destination data
    source_data['categories'] = update_source_categories(source_data['categories'], dest_data['categories'], category_mapping)

    # Update annotations in the source data to reflect the new category IDs
    source_data['annotations'] = update_annotations(source_data['annotations'], category_mapping)

    # Rename 'name' to 'file_name' in the images
    source_data['images'] = rename_image_keys(source_data['images'])

    # Save the updated source dataset
    save_json(source_data, '/home/aghosh/Projects/2PCNet/Datasets/Argoverse/Argoverse-HD/coco_labels/train.json')

    print("json file updated successfully!")