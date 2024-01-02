import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Purpose: pick images showing greatest difference for visual comparison

def load_images(folder, is_gt=False, is_cs=False):
    if is_gt:
        if is_cs:
            surfix = 'gtFine_color.png'
        else:
            surfix = 'gt_labelColor.png'
    else:
        if is_cs:
            surfix = 'leftImg8bit.png'
        else:
            surfix = 'rgb_anon.png'

    images = []

    # Walk through the directory recursively
    for root, dirs, files in os.walk(folder):
        # Pick the files only if they end with "gt_labelColor.png"
        for file in files:
            # print("root is", root)
            if file.endswith(surfix) and 'train' not in root:
                images.append(
                    os.path.join(root, file)
                    )
                
    return images


def compute_pixel_accuracy(predicted_map, gt_map):
    """
    Compute pixel accuracy for color maps.
    `predicted_map` and `gt_map` are the prediction and ground truth images, respectively.
    """
    # Ensure that the shape of predicted_map and gt_map are the same
    assert predicted_map.shape == gt_map.shape, "Shape of predicted and ground truth maps should be the same."

    # Calculate the number of matching pixels
    matching_pixels = np.sum(predicted_map == gt_map)
    
    # Total number of pixels
    total_pixels = predicted_map.size

    # Pixel accuracy
    accuracy = matching_pixels / total_pixels
    return accuracy

def compute_scores(my_pred_path, baseline_pred_path, gt_map_path, dataset='cityscapes'):
    if dataset == 'cityscapes':
        is_cs = True
    else:
        is_cs = False

    # Load predicted and GT images
    my_predicted_maps = load_images(my_pred_path, is_gt=False, is_cs=is_cs)
    baseline_predicted_maps = load_images(baseline_pred_path, is_gt=False, is_cs=is_cs)
    gt_maps = load_images(gt_map_path, is_gt=True, is_cs=is_cs)

    # Assuming all lists are sorted and of the same length
    scores_dict = {}

    for i in range(len(gt_maps)):
        my_pred_map = cv2.imread(my_predicted_maps[i])
        baseline_pred_map = cv2.imread(baseline_predicted_maps[i])

        gt_map = cv2.imread(gt_maps[i])

        my_accuracy  = compute_pixel_accuracy(my_pred_map, gt_map)
        baseline_accuracy  = compute_pixel_accuracy(baseline_pred_map, gt_map)
        # print(f"my_iou = {my_iou}, baseline_iou = {baseline_iou}")

        score = my_accuracy - baseline_accuracy

        image_filename = os.path.basename(my_predicted_maps[i])
        scores_dict[image_filename] = score

    # print("scores_dict is", scores_dict)

    # Sort images based on their score
    sorted_scores = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)

    return sorted_scores


def get_path_from_dataset(dataset):
    assert dataset in ['acdc', 'darkzurich', 'cityscapes'], print("dataset must be one of ['acdc', 'darkzurich', 'cityscapes']")

    if dataset == 'cityscapes':
        pred_map_path_baseline =  "/home/aghosh/Projects/2PCNet/Methods/DAFormer/work_dirs/local-exp80/test_11_11/preds"
        gt_map_path = "/home/aghosh/Projects/2PCNet/Datasets/cityscapes/gtFine/val"
        ours_map_path = "/home/aghosh/Projects/2PCNet/Methods/DAFormer/work_dirs/local-exp88/test_11_11/preds"

    # NOTE: this is for cityscapes to acdc
    elif dataset == 'acdc':
        pred_map_path_baseline = '/home/aghosh/Projects/2PCNet/Methods/DAFormer/work_dirs/local-exp90/231025_1230_cs2acdc_dacs_a999_fdthings_rcs001_cpl_daformer_sepaspp_mitb5_poly10warm_s0_87f3d/preds'
        gt_map_path = '/home/aghosh/Projects/2PCNet/Datasets/acdc/gt'
        ours_map_path = "/home/aghosh/Projects/2PCNet/Methods/DAFormer/work_dirs/local-exp98/231107_0010_cs2acdc_dacs_a999_fdthings_rcs001_cpl_daformer_sepaspp_mitb5_poly10warm_s0_119f2/preds"

    elif dataset == 'darkzurich':
        pred_map_path_baseline = "/home/aghosh/Projects/2PCNet/Methods/DAFormer/work_dirs/local-exp80/231025_1229_cs2dzur_dacs_a999_fdthings_rcs001_cpl_daformer_sepaspp_mitb5_poly10warm_s0_c4e21/preds/night/GOPR0356"
        gt_map_path = "/home/aghosh/Projects/2PCNet/Datasets/dark_zurich/gt/val/night/GOPR0356"
        ours_map_path = "/home/aghosh/Projects/2PCNet/Methods/DAFormer/work_dirs/local-exp88/231108_0047_cs2dzur_dacs_a999_fdthings_rcs001_cpl_daformer_sepaspp_mitb5_poly10warm_s0_d1027/preds/night/GOPR0356"


    sorted_scores = compute_scores(ours_map_path, pred_map_path_baseline, gt_map_path, dataset=dataset)

    # print("sorted_scores is", sorted_scores)

    print("Top 5 images with highest score:")
    for i in range(5):
        print(sorted_scores[i])


dataset = 'acdc' # ['acdc', 'darkzurich', 'cityscapes']
get_path_from_dataset(dataset)


# Top 5 for DarkZurich
# ('GOPR0356_frame_000333_rgb_anon.png', 0.08549864969135801)
# ('GOPR0356_frame_000366_rgb_anon.png', 0.07861641589506169)
# ('GOPR0356_frame_000357_rgb_anon.png', 0.06470936213991768)
# ('GOPR0356_frame_000354_rgb_anon.png', 0.06083140432098766)
# ('GOPR0356_frame_000448_rgb_anon.png', 0.04724778163580251)


# Top5 for Cityscapes
# Top 5 images with highest score:
# ('frankfurt_000001_034816_leftImg8bit.png', 0.034333229064941406)
# ('frankfurt_000001_075984_leftImg8bit.png', 0.030917644500732422)
# ('lindau_000054_000019_leftImg8bit.png', 0.022424856821696038)
# ('frankfurt_000001_017459_leftImg8bit.png', 0.01825555165608722)
# ('frankfurt_000000_011007_leftImg8bit.png', 0.013366063435872433)

# Top5 for ACDC
# ('GP020607_frame_000149_rgb_anon.png', 0.30357622813786006)
# ('GP020607_frame_000162_rgb_anon.png', 0.27069235468106995)
# ('GOPR0606_frame_000202_rgb_anon.png', 0.2650567451131688)
# ('GP010607_frame_000926_rgb_anon.png', 0.2561885931069959)
# ('GOPR0606_frame_000213_rgb_anon.png', 0.2402490033436214)
