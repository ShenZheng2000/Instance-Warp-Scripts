from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
import sys


def coco_mAP_dif(results_json, gt_json, model_name=None, tod=None):

    # NOTE: Assume det file is not in coco format

    annType = 'bbox'

    cocoGt = COCO(gt_json)
    cocoDt = cocoGt.loadRes(results_json)

    imgIds = sorted(cocoGt.getImgIds())
    # print("=====================================")
    # print(imgIds)
    # print("=====================================")

    objs = ['pedestrian', 'rider', 'car', 'truck', 'bus', 
            'train',
            'motorcycle', 'bicycle', 'traffic light', 'traffic sign'] 

    # Get category ids for each object type
    catIds = cocoGt.getCatIds(catNms=objs)
    print("catIds is", catIds)

    assert len(catIds) == len(objs), "Some categories from 'objs' were not found in the COCO dataset!"

    output_file_path = f"txt/{model_name}_{tod}.txt"
    with open(output_file_path, "w") as f:

        # Redirect the print output of summarize() to the file for 'All objects'
        old_stdout = sys.stdout
        sys.stdout = f

        # Evaluation for all objects
        print("\nEvaluating for all objects\n")
        cocoEvalAll = COCOeval(cocoGt, cocoDt, annType)
        cocoEvalAll.params.imgIds = imgIds
        cocoEvalAll.params.catIds = catIds
        cocoEvalAll.evaluate()
        cocoEvalAll.accumulate()
        cocoEvalAll.summarize()

        sys.stdout = old_stdout
        print("Evaluating for all objects done!")

        for i, obj in enumerate(objs):
            f.write(f"\nEvaluating for {i} {obj}\n")
            
            cocoEval = COCOeval(cocoGt, cocoDt, annType)
            cocoEval.params.imgIds = imgIds
            cocoEval.params.catIds = [catIds[i]]
            cocoEval.evaluate()
            cocoEval.accumulate()
            
            # Redirect the print output of summarize() to the file
            old_stdout = sys.stdout
            sys.stdout = f
            cocoEval.summarize()
            sys.stdout = old_stdout
            print(f"Evaluating for {obj} done!")
            
    print(f"Results saved to {output_file_path}")


# model_name = "acdc_11_6_baseline"
# model_name = "acdc_11_6_bbox"
# model_name = "acdc_11_6_fovea"
# model_name = "acdc_11_6_tpp"

# results_json = f"/home/aghosh/Projects/2PCNet/Methods/Night-Object-Detection/outputs/{model_name}/inference/coco_instances_results.json"
# gt_json = "/home/aghosh/Projects/2PCNet/Datasets/acdc/gt_detection/val.json"

# tods = [
#         # "day", 
#         # "clear"
#         # "day_bad_weather",
#         "clear_night"
#         ]

# for tod in tods:
#     if tod == "day":
#         model_names = [
#             "pretrained",
#             "warp_aug_9_12",
#             "warp_aug_8_2",
#             "bdd100k_9_22_v1"
#         ]
#     elif tod == "clear":
#         model_names = [
#             "bdd100k_10_18_baseline",
#             "bdd100k_10_18_fovea",
#             "bdd100k_10_18_tpp",
#             "bdd100k_10_18_bbox"
#         ]
#     elif tod == 'day_bad_weather':
#         model_names = [
#             "pretrained",
#             "bdd100k_9_22_v1"
#         ]
#     elif tod == 'clear_night':
#         model_names = [
#             "bdd100k_10_18_baseline",
#             "bdd100k_10_18_bbox"
#         ]
#     else:
#         model_names = []  # Add model names for other 'tod' values if needed

#     for model_name in model_names:
#         results_json = f"/home/aghosh/Projects/2PCNet/Methods/Night-Object-Detection/outputs/{model_name}/{tod}/inference/coco_instances_results.json"
#         gt_json = f"/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_{tod}.json"

#         coco_mAP_dif(results_json, gt_json, model_name=model_name, tod=tod)


# For all experiments: [model_names, tod]
    # 2PCNet (clear to dense foggy)                 [dense_foggy_12_12_baseline, dense_foggy]
    # 2PCNet + DehazeFormer (clear to dense foggy)  [dense_foggy_12_12_baseline, dense_foggy_dehazeformer]
    # 2PCNet + Ours (clear to dense foggy)          [dense_foggy_12_12_bbox, dense_foggy]

    # 2PCNet (day to night)                         [pretrained, night]
    # 2PCNet + SGZ (day to night)                   [pretrained, SGZ]
    # 2PCNet + Ours (day to night)                  [bdd100k_9_22_v1, night]

    # 2PCNet (day to clear night)                   [pretrained, clear_night]
    # 2PCNet + SGZ (day to clear night)             [pretrained, clear_SGZ]
    # 2PCNet + Ours (day to clear night)            [bdd100k_9_22_v1, clear_night]

    # 2PCNet (day to bad night)                     [pretrained, bad_night]
    # 2PCNet + SGZ (day to bad night)               [pretrained, bad_SGZ]
    # 2PCNet + Ours (day to bad night)              [bdd100k_9_22_v1, bad_night]

    # 2PCNet (clear to rainy)                       [bdd100k_10_18_baseline, rainy]
    # 2PCNet + SAPNet (clear to rainy)              [bdd100k_10_18_baseline, rainy_SAPNet]
    # 2PCNet + Ours (clear to rainy)                [bdd100k_10_18_bbox, rainy]

    # 2PCNet (clear to rainy day)                   [bdd100k_10_18_baseline, rainy_day]
    # 2PCNet + SAPNet (clear to rainy day)          [bdd100k_10_18_baseline, rainy_day_SAPNet]
    # 2PCNet + Ours (clear to rainy day)            [bdd100k_10_18_bbox, rainy_day]

    # 2PCNet (clear to rainy night)                 [bdd100k_10_18_baseline, rainy_night]
    # 2PCNet + SAPNet (clear to rainy night)        [bdd100k_10_18_baseline, rainy_night_SAPNet]
    # 2PCNet + Ours (clear to rainy night)          [bdd100k_10_18_bbox, rainy_night]


model_names = [
    "dense_foggy_12_12_baseline",
    "dense_foggy_12_12_bbox",
    # "pretrained",
    # "bdd100k_9_22_v1",
    # "bdd100k_10_18_baseline",
    # "bdd100k_10_18_bbox",
]

for model_name in model_names:
        
        # TODO: do this separate due to label mismatch
        if model_name == "dense_foggy_12_12_baseline":
            tods = ["dense_foggy",
                    "dense_foggy_dehazeformer"]
        elif model_name == "dense_foggy_12_12_bbox":
            tods = ["dense_foggy"]
        elif model_name == "pretrained":
            tods = [
                    "night",
                    "SGZ",
                    "clear_night",
                    "clear_SGZ",
                    "bad_night",
                    "bad_SGZ"
                    ]
        elif model_name == "bdd100k_9_22_v1":
            tods = [
                    "night",
                    "clear_night",
                    "bad_night"
                    ]
        elif model_name == "bdd100k_10_18_baseline":
            tods = [
                    "rainy",
                    "rainy_SAPNet",
                    "rainy_day",
                    "rainy_day_SAPNet",
                    "rainy_night",
                    "rainy_night_SAPNet"
                    ]
        elif model_name == "bdd100k_10_18_bbox":
            tods = [
                    "rainy",
                    "rainy_day",
                    "rainy_night"
                    ]
            
        for tod in tods:
            results_json = f"/home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/{model_name}/{tod}/inference/coco_instances_results.json"

            # remove SAPNet or SGZ to get tod_new to match gt_json file
            tod_new = tod.replace("SGZ", "night").replace("_SAPNet", "")

            gt_json = f"/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_{tod_new}.json"

            if 'dense_foggy' in tod:
                gt_json = f"/home/aghosh/Projects/2PCNet/Datasets/dense/coco_labels/val_dense_fog.json"

            coco_mAP_dif(results_json, gt_json, model_name=model_name, tod=tod)
