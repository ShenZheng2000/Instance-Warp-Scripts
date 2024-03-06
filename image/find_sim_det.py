import cv2
import numpy as np
import os

# Paths to the folders
# folder = '/longdata/anurag_storage/2PCNet/2PCNet/outputs/bdd100k_9_22_v1/night/inference'
folder = '/longdata/anurag_storage/2PCNet/2PCNet/outputs/bdd100k_10_18_bbox/rainy/inference'
folder_X = f'{folder}/visual'
folder_Y = f'{folder}/visual_gt'

# List to hold (difference, image1, image2) tuples
differences = []

# Load each image pair and compute the L2 difference
for filename in os.listdir(folder_X):
    if filename.endswith(".jpg"):
        path_X = os.path.join(folder_X, filename)
        path_Y = os.path.join(folder_Y, filename)

        # Load images
        img_X = cv2.imread(path_X)
        img_Y = cv2.imread(path_Y)

        # Resize images to the smallest among the two for consistency
        height_X, width_X = img_X.shape[:2]
        height_Y, width_Y = img_Y.shape[:2]
        new_width = min(width_X, width_Y)
        new_height = min(height_X, height_Y)
        img_X_resized = cv2.resize(img_X, (new_width, new_height))
        img_Y_resized = cv2.resize(img_Y, (new_width, new_height))

        # Compute L2 difference
        difference = np.linalg.norm(img_X_resized - img_Y_resized)

        # Store the result
        differences.append((difference, filename))

# Sort the list of differences
differences.sort(key=lambda x: x[0])

# Select the top 10 pairs with the smallest differences
top_10_pairs = differences[:10]

# Print the results
for diff, filename in top_10_pairs:
    print(f"{filename} has sim. of {diff}")


# # Day
# Image pair: c5121aec-f19f3e8d.jpg has a similarity score (L2 difference) of 24062.42814015244
# Image pair: c927d51b-43e6a4e8.jpg has a similarity score (L2 difference) of 32474.67099140498
# Image pair: c4d7185b-6c141918.jpg has a similarity score (L2 difference) of 36702.39189753169
# Image pair: b6658d33-adfea9cf.jpg has a similarity score (L2 difference) of 37338.73404388531
# Image pair: c1924b4e-09f3abc2.jpg has a similarity score (L2 difference) of 38213.07961941827
# Image pair: bac8434c-a3f0f643.jpg has a similarity score (L2 difference) of 39216.825368711325
# Image pair: b1d7b3ac-afa57f22.jpg has a similarity score (L2 difference) of 39918.02265894442
# Image pair: b56f50cd-07390326.jpg has a similarity score (L2 difference) of 39985.45769401671
# Image pair: bf80a27d-159d64f6.jpg has a similarity score (L2 difference) of 40050.49315551558
# Image pair: c3949a9e-7ee214aa.jpg has a similarity score (L2 difference) of 42766.4962909051
    
# # Rainy
# c1924b4e-09f3abc2.jpg has sim. of 38413.85290490919
# bac8434c-a3f0f643.jpg has sim. of 40326.99725990022
# bd812175-fc557aa4.jpg has sim. of 48427.80563890955
# c7640ee1-0cbc6ec0.jpg has sim. of 49457.86996019946
# c4891df0-24371ae1.jpg has sim. of 49712.09915101152
# c5853065-e066b724.jpg has sim. of 50048.780075042785
# c717fdbd-9b7ef8e2.jpg has sim. of 50120.712494935666
# c5a178bf-5a656bed.jpg has sim. of 52484.63949576105
# c2d84b6d-5b9fc9f6.jpg has sim. of 53471.76233302957
# c1617c3b-c295ec43.jpg has sim. of 54404.541051276225