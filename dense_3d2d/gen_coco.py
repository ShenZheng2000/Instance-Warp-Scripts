import os
import cv2
import json

# DONE: generate json for all images
# DONE: visualize some images using this json
# DONE: train/test split

def map_category(cat_name):
    category_mapping = {
        'PassengerCar': 'car',
        'Vehicle_is_group': 'car',
        'PassengerCar_is_group': 'car',
        'Vehicle': 'car',
        'LargeVehicle': 'truck',
        'LargeVehicle_is_group': 'truck',
        'Pedestrian': 'pedestrian',
        'person': 'pedestrian',
        'Pedestrian_is_group': 'pedestrian',
        'RidableVehicle': 'bicycle',
        'RidableVehicle_is_group': 'bicycle'
    }
    return category_mapping.get(cat_name, None)

def get_coco_categories():
    return [
        {"id": 1, "name": "pedestrian"},
        {"id": 2, "name": "rider"},
        {"id": 3, "name": "car"},
        {"id": 4, "name": "truck"},
        {"id": 5, "name": "bus"},
        {"id": 6, "name": "train"},
        {"id": 7, "name": "motorcycle"},
        {"id": 8, "name": "bicycle"},
        {"id": 9, "name": "traffic light"},
        {"id": 10, "name": "traffic sign"}
    ]

if __name__ == "__main__":
    base_img_dir = "/longdata/anurag_storage/DENSE/cam_stereo_left_lut"
    base_label_dir = "/longdata/anurag_storage/DENSE/gt_labels/cam_left_labels_TMP"

    coco_output = {
        "info": {"description": "COCO-like dataset"},
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": get_coco_categories()
    }

    image_id = 0
    ann_id = 0
    for img_basename in os.listdir(base_img_dir):
        if not img_basename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        label_basename = os.path.splitext(img_basename)[0] + ".txt"
        im_path = os.path.join(base_img_dir, img_basename)
        label_path = os.path.join(base_label_dir, label_basename)

        img = cv2.imread(im_path)
        height, width, _ = img.shape

        coco_output["images"].append({
            "id": image_id,
            "width": width,
            "height": height,
            "file_name": img_basename,
        })

        with open(label_path, 'r') as f:
            labels = f.readlines()
            labels = [l.strip() for l in labels]
            labels = [l.split() for l in labels]

        for l in labels:
            cat_name = map_category(l[0])
            if cat_name is not None:
                trunc = l[1]
                occ = l[2]
                bbox = l[4:8]
                bbox = [float(b) for b in bbox]
                bbox[2] = bbox[2] - bbox[0]  # width
                bbox[3] = bbox[3] - bbox[1]  # height

                ann = {
                    "id": ann_id,
                    "image_id": image_id,
                    "category_id": next((cat["id"] for cat in coco_output["categories"] if cat["name"] == cat_name), None),
                    "bbox": bbox,
                    "area": bbox[2] * bbox[3],
                    "iscrowd": 0
                }
                coco_output["annotations"].append(ann)
                ann_id += 1

        image_id += 1

    # Saving annotations in COCO format
    with open('coco_annotations.json', 'w') as f:
        json.dump(coco_output, f, indent=4)

    print("Annotations saved in COCO format to coco_annotations.json")
