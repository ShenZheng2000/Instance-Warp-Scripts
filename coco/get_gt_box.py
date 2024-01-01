from pycocotools.coco import COCO

# Load the COCO format JSON file
coco = COCO('/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/train_day.json')

# Specify the image file name for which you want the ground truth bounding boxes
# image_file_name = '0a0a0b1a-7c39d841.jpg'  # Replace with the actual image file name
image_file_name = '0a0c3694-24fe9c8d.jpg'  # Replace with the actual image file name

# Get the image info for the specified image file name
img_info = next(item for item in coco.dataset['images'] if item["file_name"] == image_file_name)

# Check if we found the image
if img_info is None:
    raise ValueError("Image not found in the dataset.")

# Get the annotation IDs associated with the image
ann_ids = coco.getAnnIds(imgIds=img_info['id'])

# Load the annotations
annotations = coco.loadAnns(ann_ids)

# Extract the ground truth bounding boxes
gt_bboxes = [ann['bbox'] for ann in annotations]

# Now, gt_bboxes contains the ground truth bounding boxes for the specified image
print(gt_bboxes)
