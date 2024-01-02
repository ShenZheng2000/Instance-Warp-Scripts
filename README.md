# Utility Scripts

This repository hosts utility scripts for image warping research. 

Key files are summarized in this readme

Consult the python files in each subfolder for further details.

# bdd

Obtain coco-format json of specific weather or tod

(1) Convert bdd-format to coco-format:  `bdd/bdd2coco.py`

(2) Filter coco-format json based on weather and tod: `bdd/filter_file.py`

# sem_seg

Generate json containing bboxes for instance-level warping: 

(1) Run: `sem_seg/seg_to_bbox.py`


# coco

Visualize bboxes (and get results) on images

(1) Run detection on image

(2) Get category-wise results: `coco/coco_mAP_simple.py`

(3) Get bboxes visualizations: `coco/vis_det_each.sh`

# video

Visualize bboxes on videos

(1) Convert video to image: `video/video2image.py`

(2) Generate pseduo-json for images: `jsons/create_empty_json.py`

(3) Run detection on image

(4) Visualize detected images: `coco/vis_det_each.sh`

(5) Merge images to video: `video/image2video.py`

# dense_3d2d

Obtain 2d coco annotations from the DENSE dataset

(1) Get coco-format jsons with 2D bboxes: `dense_3d2d/gen_coco.py`

(2) Visualize 2D bboxes for debug: `dense_3d2d/vis_many.py`

(3) Count the occurence for each category: `dense_3d2d/count_category.py`

(4) Split into train/test based on ratio and tod constraints: `dense_3d2d/train_test_split.py`