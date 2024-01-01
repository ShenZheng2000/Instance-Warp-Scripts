import os
import shutil
from random import sample
import random


# TODO: no use for now. debug later

def create_subset_with_subfolders(img_dir, ann_dir, target_img_dir, target_ann_dir, subset_ratio, seed=0):
    """
    Copies a subset of image files and their corresponding annotations from the original 
    directories to corresponding subfolders in the target directories, maintaining the directory structure.
    
    Parameters:
    - img_dir (str): The directory containing the original images.
    - ann_dir (str): The directory containing the original annotations.
    - target_img_dir (str): The directory where the subset of image files will be copied to.
    - target_ann_dir (str): The directory where the subset of annotation files will be copied to.
    - subset_ratio (float): The ratio of files to be copied (e.g., 0.25 for 25%).
    - seed (int): The seed for the random number generator to ensure reproducibility.
    """
    # Set the seed for reproducibility
    random.seed(seed)

    # Get all image files and calculate how many to select based on the subset ratio
    all_images = [f for f in os.listdir(img_dir) if f.lower().endswith('leftimg8bit.png')]
    num_files_to_select = int(len(all_images) * subset_ratio)
    
    # Randomly select a subset of image files
    selected_images = sample(all_images, num_files_to_select)

    # Copy the selected image files and their corresponding annotations
    for image_name in selected_images:
        # Construct the base name without the extension and suffix
        base_name = image_name.replace('_leftImg8bit.png', '')

        # Copy the image file
        src_img_path = os.path.join(img_dir, image_name)
        dst_img_path = os.path.join(target_img_dir, image_name)
        if not os.path.exists(target_img_dir):
            os.makedirs(target_img_dir)
        shutil.copy(src_img_path, dst_img_path)

        # Find and copy all related annotation files
        for ann_suffix in ['_gtFine_labelTrainIds.png', '_gtFine_color.png', '_gtFine_instanceIds.png']:
            ann_name = f"{base_name}{ann_suffix}"
            src_ann_path = os.path.join(ann_dir, ann_name)
            dst_ann_path = os.path.join(target_ann_dir, ann_name)
            if not os.path.exists(target_ann_dir):
                os.makedirs(target_ann_dir)
            if os.path.exists(src_ann_path):  # Check if the annotation file exists
                shutil.copy(src_ann_path, dst_ann_path)

# Example usage
# Define the paths for the Cityscapes dataset
original_img_dir = '/path/to/original/images'  # Replace with your actual path to images
original_ann_dir = '/path/to/original/annotations'  # Replace with your actual path to annotations

# Define the paths for the target directories
target_img_dir = '/path/to/target/images'  # Replace with your actual target path for images
target_ann_dir = '/path/to/target/annotations'  # Replace with your actual target path for annotations

# Define the subset ratio (e.g., 0.25 for 25%)
subset_ratio = 0.25  # Replace with your desired subset ratio

# Copy the subset of images and annotations
create_subset_with_subfolders(original_img_dir, original_ann_dir, target_img_dir, target_ann_dir, subset_ratio)
