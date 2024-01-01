from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
import sys


def coco_mAP_dif(results_json, gt_json, model_name=None):

    # NOTE: Assume det file is not in coco format

    annType = 'bbox'

    cocoGt = COCO(gt_json)
    cocoDt = cocoGt.loadRes(results_json)

    imgIds = sorted(cocoGt.getImgIds())


    objs = ['pedestrian', 'rider', 'car', 'truck', 'bus', 'train', 
            'motorcycle', 'bicycle', 'traffic light', 'traffic sign'] 
    
            # NOTE: for pretrained model: not work with current label
    # objs = ['person', 'rider', 'car', 'truck', 'bus', 'train', 'motor', 'bike', 'traffic light', 'traffic sign'] # for mine label

    # Get category ids for each object type
    catIds = cocoGt.getCatIds(catNms=objs)

    output_file_path = f"txt/{model_name}.txt"
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



if __name__ == '__main__':
    model_names = [
        # ('pretrained', 'night'), 
        # ('warp_aug_9_12', 'night'), 
        # ('warp_aug_8_2', 'night'), 
        # ('bdd100k_9_22_v1', 'night'),
        # ('bdd100k_10_9_05x', 'night_05'),
        # ('bdd100k_bbox_05x_retrain', 'night_05'),
        # ('bdd100k_fovea_05x_retrain', 'night_05'),
        # ('bdd100k_tpp_05x_retrain', 'night_05'), 
        # ('bdd100k_10_18_tpp', 'rainy'),
        # ('bdd100k_10_18_bbox', 'rainy'),
        # ('bdd100k_10_18_baseline', 'rainy'),  
        # ('bdd100k_10_18_fovea', 'rainy')
    ]

    src_path = "/home/aghosh/Projects/2PCNet"
    scene_to_gt_file = {
        'night': 'val_night.json',
        'night_05': 'val_night.json',
        'rainy': 'val_rainy.json',
        'rainy05': 'val_rainy.json'
    }

    for model, scene in model_names:
        gt_json = f'{src_path}/Datasets/bdd100k/coco_labels/{scene_to_gt_file[scene]}'
        results_json = f'{src_path}/Methods/Night-Object-Detection/outputs/{model}/{scene}/inference/coco_instances_results.json'
        coco_mAP_dif(results_json, gt_json, model)