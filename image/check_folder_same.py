from PIL import Image, ImageChops
import numpy as np
import os
import sys

def compute_image_difference(image1_path, image2_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    diff = ImageChops.difference(image1, image2)
    diff = diff.convert("L")  # Convert to grayscale
    diff_array = np.array(diff)

    # Calculate the mean squared error
    mse = np.mean(diff_array ** 2)
    
    return mse

def compute_average_mse(folder1, folder2, skip_file="img.png"):
    image_files = [f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))]
    total_mse = 0
    image_count = 0  # Initialize a counter for the number of images processed

    for image_file in image_files:
        if image_file == skip_file:  # Skip the specified file
            continue
        
        image1_path = os.path.join(folder1, image_file)
        image2_path = os.path.join(folder2, image_file)
        
        if os.path.exists(image2_path):  # Check if the corresponding file exists in the second folder
            mse = compute_image_difference(image1_path, image2_path)
            total_mse += mse
            image_count += 1  # Only increment the count if an MSE was actually computed
        else:
            print(f"No corresponding file found for {image_file} in {folder2}")
    
    if image_count == 0:
        return "No images were processed."
    else:
        average_mse = total_mse / image_count
        return average_mse
    
    
# Example usage:
folder1 = "/home/aghosh/Projects/2PCNet/Methods/DAFormer/attention_maps/90/attn_stage_1"  

id = sys.argv[1]

folder2 = f"/home/aghosh/Projects/2PCNet/Methods/DAFormer/attention_maps/{id}/attn_stage_1" 

avg_mse = compute_average_mse(folder1, folder2)
print("Average mse is", avg_mse)
