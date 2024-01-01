
from tidecv import TIDE, datasets, Data
import json
import sys
import os


def transform_to_coco(dets_json_ori, gt_json, dets_json):

    # Load the current data
    with open(dets_json_ori, 'r') as f:
        data = json.load(f)

    # Load the mapping data
    with open(gt_json, 'r') as f:
        mapping_data = json.load(f)

    # Create a dictionary to map image IDs to file names and image dimensions
    id_to_filename = {}
    for img in mapping_data["images"]:
        id_to_filename[img["id"]] = (img["file_name"], img["width"], img["height"])

    # Initialize a dictionary to hold the COCO-like data
    coco_format = {
        "images": [],
        "annotations": [],
        "categories": []
    }

    # Use sets to avoid duplicate ids
    image_ids = set()
    category_ids = set()

    # Generate the "annotations" list
    for idx, item in enumerate(data):
        image_id = item['image_id']
        category_id = item['category_id']
        bbox = item['bbox']
        score = item['score']

        # add the annotation
        coco_format["annotations"].append({
            "id": idx,
            "image_id": image_id,
            "category_id": category_id,
            "bbox": bbox,
            "area": bbox[2]*bbox[3],  # assuming bbox is in format [x, y, w, h]
            "score": score,
        })

        # track the unique ids
        image_ids.add(image_id)
        category_ids.add(category_id)

    # Generate the "images" list
    for image_id in image_ids:
        file_name, width, height = id_to_filename[image_id]
        coco_format["images"].append({
            "id": image_id,
            "file_name": file_name,
            "width": width,
            "height": height
        })

    # Generate a placeholder "categories" list
    for category_id in category_ids:
        coco_format["categories"].append({
            "id": category_id,
            # We do not have this information, so placeholders are used
            "name": f"unknown_{category_id}"
        })

    # Save the COCO-like data to a new file (TODO: change this later)
    with open(dets_json, 'w') as f:
        json.dump(coco_format, f)



def cal_tide(dets_json, gt_json, out_dir):

    tide = TIDE()

    gt_data = Data('gt_data')
    det_data = Data('det_data')

    for det in gt_json['annotations']:
        image = det['image_id']
        _cls = det['category_id']
        box = det['bbox'] if 'bbox' in det else None
        mask = det['segmentation'] if 'segmentation' in det else None
        gt_data.add_ground_truth(image, _cls, box, mask)

    for det in dets_json['annotations']:
        image = det['image_id']
        _cls = det['category_id']
        score = det['score']
        box = det['bbox'] if 'bbox' in det else None
        mask = det['segmentation'] if 'segmentation' in det else None
        det_data.add_detection(image, _cls, score, box, mask)

    tide.evaluate(gt_data, det_data, mode=TIDE.BOX) # 两者通过tide对比
    tide.summarize()
    tide.plot(out_dir=out_dir)


def main():
    # dets_json_ori = '/root/autodl-tmp/Methods/UDA/outputs/light_white_100_7_1/inference/coco_instances_results.json'
    # gt_json = '/root/autodl-tmp/Datasets/bdd100k/coco_labels/val_night.json'

    # TODO: use this later
    dets_json_ori = sys.argv[1]
    gt_json = sys.argv[2]

    dets_json = dets_json_ori.replace("coco_instances_results", 'coco_instances_results_COCO')
    out_dir = os.path.dirname(dets_json_ori)

    transform_to_coco(dets_json_ori, gt_json, dets_json)
    # validate_coco_format('coco_format.json')

    with open(dets_json) as f: #加载检测结果的json文件
        dets_json = json.load(f)

    with open(gt_json) as f: # 加载标签的json文件
        gt_json = json.load(f)

    # cal_tide(dets_json, gt_json, out_dir)


if __name__ == '__main__':
    main()