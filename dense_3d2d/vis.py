import os
import cv2

if __name__=="__main__":
    # base_img_dir = "/longdata/anurag_storage/DENSE/cam_stereo_left_lut/"
    # base_label_dir = "longdata/anurag_storage/DENSE/gt_labels/cam_left_labels_TMP/"
    # all_images = os.listdir(base_img_dir)

    base_img_dir = "/longdata/anurag_storage/DENSE/cam_stereo_left_lut"
    base_label_dir = "/longdata/anurag_storage/DENSE/gt_labels/cam_left_labels_TMP"

    # https://github.com/bostondiditeam/kitti/blob/master/resources/devkit_object/readme.txt
    # https://github.com/princeton-computational-imaging/SeeingThroughFog

    # img_basename = "2018-02-03_21-02-09_00000.png"
    # img_basename = "2018-02-03_21-36-01_00300.png"
    # img_basename = "2018-02-03_21-37-59_00300.png"
    # img_basename = "2018-02-03_21-41-51_00400.png"
    # img_basename = "2019-09-11_20-58-32_00600.png"
    # img_basename = "2018-02-03_21-48-01_00100.png"
    img_basename = "2018-02-03_21-48-01_00200.png"

    label_basename = os.path.splitext(img_basename)[0] + ".txt"
    im_path = os.path.join(base_img_dir, img_basename)
    label_path = os.path.join(base_label_dir, label_basename)

    # print("im_path is", im_path)
    # print("label_path is", label_path)
    # exit()

    img = cv2.imread(im_path)
    with open(label_path, 'r') as f:
        labels = f.readlines()
        labels = [l.strip() for l in labels]
        labels = [l.split() for l in labels]

    coco_style_ann = []
    for l in labels:
        cat_name = l[0]
        trunc = l[1]
        occ = l[2]
        bbox = l[4:8]
        bbox = [float(b) for b in bbox]
        bbox[2] = bbox[2] - bbox[0]
        bbox[3] = bbox[3] - bbox[1]
        ann = {
            # "id" : ann_id,
            # "image_id" : image_id,
            # "category_id": categories_dict[cat_name],
            "truncated": float(trunc),
            "occluded": int(occ),
            "bbox": bbox,
            "alpha": 0.0
        }
        coco_style_ann.append(ann)

    for ann in coco_style_ann:
        bbox = ann["bbox"]
        bbox = [int(b) for b in bbox]
        cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0,255,0), 2)

    cv2.imwrite("test.png", img)