import os
import cv2
from glob import glob
import argparse

# Purpose: Resize all images in a directory to a specified size

# Argument parsing
parser = argparse.ArgumentParser(description='Reshape images')
parser.add_argument('--src', type=str, required=True, help='Directory to perform in-place image resize')
args = parser.parse_args()

src = args.src

target_w, target_h = 640, 360

success = 0
skipped = 0

# Walk through all directories and files in the source directory
for root, dirs, files in os.walk(src):
    for file in files:
        if file.endswith(('.jpg', '.png')):
            img_path = os.path.join(root, file)
            
            # read image
            img = cv2.imread(img_path)
            h, w, c = img.shape

            # check if image already has expected dimensions
            if h == target_h and w == target_w:
                skipped += 1
                continue

            # reshape image
            img_r = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_AREA)

            # overwrite original image
            cv2.imwrite(img_path, img_r)
            success += 1

# check # of success and skipped images
print(f"Resized {success} images")
print(f"Skipped {skipped} images")
