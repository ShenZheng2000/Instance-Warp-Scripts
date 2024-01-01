import json
import sys
import os

# Folder path containing the JSON files
folder_path = sys.argv[1]

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        # Construct the full file path
        src_json = os.path.join(folder_path, filename)
        tgt_json = src_json

        # Load COCO formatted JSON
        with open(src_json, 'r') as f:
            data = json.load(f)

        # Check if the image dimensions are already 360x640
        first_image = data['images'][0]  # Assuming at least one image exists
        if first_image['height'] == 360 and first_image['width'] == 640:
            # Skip modification if dimensions are already correct
            print("skip json")
            continue

        # Iterate over images and reduce height and width by half
        for img in data['images']:
            img['height'] //= 2
            img['width'] //= 2

        # Iterate over annotations
        for anno in data['annotations']:
            # Reduce bounding box coordinates by half
            anno['bbox'][0] /= 2  # x
            anno['bbox'][1] /= 2  # y
            anno['bbox'][2] /= 2  # width
            anno['bbox'][3] /= 2  # height

            # Recalculate area
            anno['area'] = anno['bbox'][2] * anno['bbox'][3]

            # Check if segmentation exists and is a polygon (list of lists)
            if 'segmentation' in anno and isinstance(anno['segmentation'], list) and all(isinstance(seg, list) for seg in anno['segmentation']):
                # Reduce segmentation coordinates by half
                for segment in anno['segmentation']:
                    for i in range(len(segment)):
                        segment[i] /= 2.0

        # Save modified COCO formatted JSON
        with open(tgt_json, 'w') as f:
            json.dump(data, f)
