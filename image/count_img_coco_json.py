import json

def count_images(coco_json_file):
    with open(coco_json_file, 'r') as f:
        coco_data = json.load(f)
    
    image_ids = set()
    for annotation in coco_data['annotations']:
        image_ids.add(annotation['image_id'])
    
    return len(image_ids)

# Replace 'path_to_coco_json_file' with the path to your COCO JSON file
coco_json_file = '/home/aghosh/Projects/2PCNet/Datasets/dense/coco_labels/train_dense_fog.json'
image_count = count_images(coco_json_file)
print("Number of images:", image_count)