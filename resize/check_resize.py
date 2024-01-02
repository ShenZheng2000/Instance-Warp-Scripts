import os
from PIL import Image
import sys

# Purpose: Check the resolution of all images in a folder

def check_image_resolution(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_path = os.path.join(root, file)
                image = Image.open(image_path)
                width, height = image.size
                if width != 640 or height != 360:
                    print(f"Incorrect resolution found: {image_path}")
                image.close()

# Provide the path to the folder you want to check
folder_path = sys.argv[1]
check_image_resolution(folder_path)
