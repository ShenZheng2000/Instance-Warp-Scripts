from PIL import Image, ImageChops
import numpy as np
import os
import sys

# Purpose: Compute the average MSE between two images

def compute_image_difference(image1_path, image2_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    diff = ImageChops.difference(image1, image2)
    diff = diff.convert("L")  # Convert to grayscale
    diff_array = np.array(diff)

    # Calculate the mean squared error
    mse = np.mean(diff_array ** 2)
    
    return mse

if len(sys.argv) == 3:
    image1_path = sys.argv[1]
    image2_path = sys.argv[2]
    
    mse = compute_image_difference(image1_path, image2_path)
    print(f"Mean Squared Error (MSE) between {image1_path} and {image2_path}: {mse}")
else:
    print("Usage: python image_compare.py <image1_path> <image2_path>")
