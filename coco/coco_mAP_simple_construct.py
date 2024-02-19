from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
import sys

# Purpose: compute categorical mAP using detectron2-style json file
def coco_mAP_dif(results_json, gt_json, model_name=None, tod=None):
    annType = 'bbox'

    cocoGt = COCO(gt_json)
    cocoDt = cocoGt.loadRes(results_json)

    imgIds = sorted(cocoGt.getImgIds())

    # Retrieve all category IDs from the COCO ground truth
    catIds = cocoGt.getCatIds()
    categories = cocoGt.loadCats(catIds)
    objs = [cat['name'] for cat in categories]  # List of all object names
    print("Evaluating categories:", objs)

    output_file_path = f"txt/{model_name}_{tod}.txt"
    with open(output_file_path, "w") as f:
        # Redirect the print output of summarize() to the file for 'All objects'
        old_stdout = sys.stdout
        sys.stdout = f

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
            catId = cocoGt.getCatIds(catNms=[obj])
            f.write(f"\nEvaluating for {obj}\n")
            
            cocoEval = COCOeval(cocoGt, cocoDt, annType)
            cocoEval.params.imgIds = imgIds
            cocoEval.params.catIds = catId
            cocoEval.evaluate()
            cocoEval.accumulate()
            
            # Redirect the print output of summarize() to the file
            old_stdout = sys.stdout
            sys.stdout = f
            cocoEval.summarize()
            sys.stdout = old_stdout
            print(f"Evaluating for {obj} done!")
            
    print(f"Results saved to {output_file_path}")

model_names = [
    "1_11_v1", # Sup base
    "1_12_v1", # DA
    '1_13_v1', # Sup Upper
]


for model_name in model_names:

    results_json = f"/home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/{model_name}/inference/coco_instances_results.json"

    gt_json = f"/home/aghosh/Projects/2PCNet/Datasets/data/annotations/geographic_da/instances_test.json"

    coco_mAP_dif(results_json, gt_json, model_name=model_name, tod='')
