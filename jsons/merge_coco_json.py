import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)
        
def merge_coco_json(file_path1, file_path2, merged_file_path):
    # Load both JSON files
    coco1 = load_json(file_path1)
    coco2 = load_json(file_path2)

    # Initialize the merged COCO format
    merged_coco = {
        "images": coco1["images"],
        "annotations": coco1["annotations"],
        "categories": coco1.get("categories", [])
    }

    # Get the highest image ID from the first dataset
    last_image_id = max(image['id'] for image in coco1["images"])

    # Update image IDs in the second dataset and add them to the merged dataset
    id_mapping = {}
    for image in coco2["images"]:
        old_id = image['id']
        new_id = last_image_id + old_id + 1
        id_mapping[old_id] = new_id
        image['id'] = new_id
        merged_coco["images"].append(image)

    # Update annotation IDs and their image references
    last_annotation_id = max(annotation['id'] for annotation in coco1["annotations"])
    for annotation in coco2["annotations"]:
        annotation['id'] = last_annotation_id + annotation['id'] + 1
        annotation['image_id'] = id_mapping[annotation['image_id']]
        merged_coco["annotations"].append(annotation)

    # Save the merged COCO JSON
    save_json(merged_coco, merged_file_path)

# Example usage
merge_coco_json('/home/aghosh/Projects/2PCNet/Datasets/data/annotations/geographic_da/instances_pretrain.json',
                 '/home/aghosh/Projects/2PCNet/Datasets/data/annotations/geographic_da/instances_unsupervised_with_gt.json', 
                 '/home/aghosh/Projects/2PCNet/Datasets/data/annotations/geographic_da/instances_all.json')
