
# # Ours (day2night)
# python vis_det_each.py \
#     /home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/100k/val \
#     /longdata/anurag_storage/2PCNet/2PCNet/outputs_11_14_det_ckpts/bdd100k_9_22_v1/night/inference/coco_instances_results.json \
#     /home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_night.json

# # Baseline (day2night)
# python vis_det_each.py \
#     /home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/100k/val \
#     /longdata/anurag_storage/2PCNet/2PCNet/outputs_11_14_det_ckpts/pretrained/night/inference/coco_instances_results.json \
#     /home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_night.json

# # # Ours (clear2rainy)
python vis_det_each.py \
    /home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/100k/val \
    /longdata/anurag_storage/2PCNet/2PCNet/outputs/bdd100k_10_18_bbox/rainy/inference/coco_instances_results.json \
    /home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_rainy.json

# # Baseline (clear2rainy)
# python vis_det_each.py \
#     /home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/100k/val \
#     /longdata/anurag_storage/2PCNet/2PCNet/outputs_11_14_det_ckpts/bdd100k_10_18_baseline/rainy/inference/coco_instances_results.json \
#     /home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_rainy.json

# # Ours (Day)
# python vis_det_each.py \
#     /home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/100k/val \
#     /longdata/anurag_storage/2PCNet/2PCNet/outputs_11_14_det_ckpts/bdd100k_9_22_v1/day/inference/coco_instances_results.json \
#     /home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_day.json


# # Baseline (Boreas)
# python vis_det_each.py \
#     /home/aghosh/Projects/2PCNet/Datasets/boreas/images/test \
#     /home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/boreas_snow_12_16_baseline/inference/coco_instances_results.json \
#     /home/aghosh/Projects/2PCNet/Datasets/boreas/coco_labels/test_snowy.json


# # Ours (Boreas)
# python vis_det_each.py \
#     /home/aghosh/Projects/2PCNet/Datasets/boreas/images/test \
#     /home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/boreas_snow_12_16_bbox/inference/coco_instances_results.json \
#     /home/aghosh/Projects/2PCNet/Datasets/boreas/coco_labels/test_snowy.json

# # Baseline (Dense)
# python vis_det_each.py \
#     /home/aghosh/Projects/2PCNet/Datasets/dense/cam_stereo_left_lut_fog_val \
#     /home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/dense_foggy_12_12_baseline/inference/coco_instances_results.json \
#     /home/aghosh/Projects/2PCNet/Datasets/dense/coco_labels/val_dense_fog.json

# # Ours (Dense)
# python vis_det_each.py \
#     /home/aghosh/Projects/2PCNet/Datasets/dense/cam_stereo_left_lut_fog_val \
#     /home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/dense_foggy_12_12_bbox/inference/coco_instances_results.json \
#     /home/aghosh/Projects/2PCNet/Datasets/dense/coco_labels/val_dense_fog.json


# # gm_rainy_day
# python vis_det_each.py \
#     /home/aghosh/Projects/2PCNet/Datasets/gm/rainy/day/images \
#     /home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/bdd100k_10_18_baseline/gm_rainy_day/inference/coco_instances_results.json \
#     /home/aghosh/Projects/2PCNet/Datasets/gm/coco_labels/rainy_day.json

# python vis_det_each.py \
#     /home/aghosh/Projects/2PCNet/Datasets/gm/rainy/day/images \
#     /home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/bdd100k_10_18_bbox/gm_rainy_day/inference/coco_instances_results.json \
#     /home/aghosh/Projects/2PCNet/Datasets/gm/coco_labels/rainy_day.json

# # gm night baseline
# python vis_det_each.py \
#     /home/aghosh/Projects/2PCNet/Datasets/gm/rainy/night/images \
#     /home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/bdd100k_10_18_baseline/gm_rainy_night/inference/coco_instances_results.json \
#     /home/aghosh/Projects/2PCNet/Datasets/gm/coco_labels/rainy_night.json

# # gm night ours
# python vis_det_each.py \
#     /home/aghosh/Projects/2PCNet/Datasets/gm/rainy/night/images \
#     /home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/bdd100k_10_18_bbox/gm_rainy_night/inference/coco_instances_results.json \
#     /home/aghosh/Projects/2PCNet/Datasets/gm/coco_labels/rainy_night.json

# # gm foggy day baseline
# python vis_det_each.py \
#     /home/aghosh/Projects/2PCNet/Datasets/gm/foggy/day/images \
#     /home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/dense_foggy_12_12_baseline/gm_foggy_day/inference/coco_instances_results.json \
#     /home/aghosh/Projects/2PCNet/Datasets/gm/coco_labels/foggy_day.json

# # gm foggy day ours
# python vis_det_each.py \
#     /home/aghosh/Projects/2PCNet/Datasets/gm/foggy/day/images \
#     /home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/dense_foggy_12_12_bbox/gm_foggy_day/inference/coco_instances_results.json \
#     /home/aghosh/Projects/2PCNet/Datasets/gm/coco_labels/foggy_day.json