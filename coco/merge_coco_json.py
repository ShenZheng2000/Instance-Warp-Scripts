# import json

# def merge_coco_jsons(json1_path, json2_path, merged_json_path):
#     # Load the two COCO data files
#     with open(json1_path, 'r') as f:
#         coco1_data = json.load(f)
#     with open(json2_path, 'r') as f:
#         coco2_data = json.load(f)

#     # Initialize the merged COCO data with the contents of the first file
#     merged_data = coco1_data

#     # Update image IDs for the second dataset to follow the first dataset's IDs
#     last_image_id = max([img['id'] for img in coco1_data['images']])
#     image_id_mapping = {img['id']: img['id'] + last_image_id for img in coco2_data['images']}
#     for img in coco2_data['images']:
#         img['id'] = image_id_mapping[img['id']]

#     # Update annotation IDs for the second dataset to follow the first dataset's IDs
#     last_annotation_id = max([anno['id'] for anno in coco1_data['annotations']])
#     for anno in coco2_data['annotations']:
#         anno['image_id'] = image_id_mapping[anno['image_id']]  # Update image IDs in annotations
#         anno['id'] += last_annotation_id

#     # Merge categories (assuming they are the same and no need to change IDs)
#     # If categories can differ, you would need to merge and reassign IDs similarly to images and annotations

#     # Merge images and annotations
#     merged_data['images'].extend(coco2_data['images'])
#     merged_data['annotations'].extend(coco2_data['annotations'])

#     # Write the merged COCO data to a new JSON file
#     with open(merged_json_path, 'w') as f:
#         json.dump(merged_data, f)

# # Paths to your JSON files and the desired output path
# json1_path = '/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_day.json'
# json2_path = '/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_night.json'
# merged_json_path = '/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val.json'

# # Merge the JSON files
# merge_coco_jsons(json1_path, json2_path, merged_json_path)
