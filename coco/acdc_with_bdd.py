# # Purpose: transform acdc label to fit with bdd's categories and ids, 

import sys
import os
import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def create_category_mapping(source_categories, target_categories):
    mapping = {}
    unmatched_categories = source_categories.copy()  # Start with a copy of source categories

    # Iterate over source categories and find matches or close matches
    for source_cat in source_categories:
        for target_cat in target_categories:
            # Direct match or close match (e.g., 'pedestrian' in source is 'person' in target)
            if source_cat["name"] == target_cat["name"] or \
               (source_cat["name"] == "pedestrian" and target_cat["name"] == "person"):
                mapping[target_cat["id"]] = source_cat["id"]
                if source_cat in unmatched_categories:
                    unmatched_categories.remove(source_cat)  # Remove matched categories
                break

    return mapping, unmatched_categories


def update_categories(target_categories, source_categories, mapping, unmatched_categories):
    updated_categories = []

    # Keep track of the source IDs that have been used
    used_source_ids = set(mapping.values())
    source_ids_to_names = {cat["id"]: cat["name"] for cat in source_categories}

    # Update IDs in the existing target categories based on the mapping
    for cat in target_categories:
        source_id = mapping.get(cat["id"])
        if source_id:
            # Change the target category ID to the source category ID
            cat["id"] = source_id
            # If the original name was "pedestrian", preserve it
            if source_ids_to_names.get(source_id) == "pedestrian":
                cat["name"] = "pedestrian"
        updated_categories.append(cat)

    # Get the maximum id from the updated categories to avoid conflicts
    max_id = max([cat["id"] for cat in updated_categories], default=0)

    # Append unmatched source categories with new IDs to avoid collisions
    for new_cat in unmatched_categories:
        # Increment max_id for new unique IDs
        max_id += 1
        new_cat["id"] = max_id
        updated_categories.append(new_cat)

    return updated_categories

def update_annotations(target_annotations, mapping):
    for ann in target_annotations:
        # Update the category_id using the mapping from ACDC to BDD, if available
        ann["category_id"] = mapping.get(ann["category_id"], ann["category_id"])
    return target_annotations

if __name__ == "__main__":
    train_or_val = sys.argv[1]
    wea_tod = sys.argv[2]

    # Load source and target datasets
    source_json_path = '/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_rainy.json'
    # target_json_path = f'/home/aghosh/Projects/2PCNet/Datasets/acdc/gt_detection/{wea_tod}/instancesonly_{wea_tod}_{train_or_val}_gt_detection.json'
    target_json_path = '/home/aghosh/Projects/2PCNet/Datasets/Argoverse/Argoverse-HD/annotations/minival.json'
    source_data = load_json(source_json_path)
    target_data = load_json(target_json_path)

    # Create a mapping from target to source category IDs and find unmatched categories
    category_mapping, unmatched_categories = create_category_mapping(source_data["categories"], target_data["categories"])

    # print("category_mapping is", category_mapping); exit()

    # Update target "categories" to be consistent with source and add unmatched categories
    # target_data["categories"] = update_categories(target_data["categories"], category_mapping, unmatched_categories)
    target_data["categories"] = update_categories(target_data["categories"], source_data["categories"], category_mapping, unmatched_categories)

    # print("target_data['categories'] is", target_data["categories"]); exit()

    # Update target "annotations" based on changed category IDs
    target_data["annotations"] = update_annotations(target_data["annotations"], category_mapping)

    # Update the images file_name
    # target_data["images"] = update_images(target_data["images"])

    # Save the modified target dataset as a new JSON file
    # save_path = f'/home/aghosh/Projects/2PCNet/Datasets/acdc/gt_detection/{train_or_val}_{wea_tod}.json'
    save_path = '/home/aghosh/Projects/2PCNet/Datasets/Argoverse/Argoverse-HD/coco_labels/minival.json'
    print(f"Saving updated dataset to {save_path}")
    save_json(target_data, save_path)


