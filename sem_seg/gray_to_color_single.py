# # NOTE: modified from DAFormer/mmseg/models/utils/visualization.py

# import numpy as np
# import torch
# from matplotlib import pyplot as plt
# from PIL import Image
# from torchvision.utils import save_image  # Import save_image from torchvision

# Cityscapes_palette = [
#     128, 64, 128, 244, 35, 232, 70, 70, 70, 102, 102, 156, 190, 153, 153, 153,
#     153, 153, 250, 170, 30, 220, 220, 0, 107, 142, 35, 152, 251, 152, 70, 130,
#     180, 220, 20, 60, 255, 0, 0, 0, 0, 142, 0, 0, 70, 0, 60, 100, 0, 80, 100,
#     0, 0, 230, 119, 11, 32, 128, 192, 0, 0, 64, 128, 128, 64, 128, 0, 192, 128,
#     128, 192, 128, 64, 64, 0, 192, 64, 0, 64, 192, 0, 192, 192, 0, 64, 64, 128,
#     192, 64, 128, 64, 192, 128, 192, 192, 128, 0, 0, 64, 128, 0, 64, 0, 128,
#     64, 128, 128, 64, 0, 0, 192, 128, 0, 192, 0, 128, 192, 128, 128, 192, 64,
#     0, 64, 192, 0, 64, 64, 128, 64, 192, 128, 64, 64, 0, 192, 192, 0, 192, 64,
#     128, 192, 192, 128, 192, 0, 64, 64, 128, 64, 64, 0, 192, 64, 128, 192, 64,
#     0, 64, 192, 128, 64, 192, 0, 192, 192, 128, 192, 192, 64, 64, 64, 192, 64,
#     64, 64, 192, 64, 192, 192, 64, 64, 64, 192, 192, 64, 192, 64, 192, 192,
#     192, 192, 192, 32, 0, 0, 160, 0, 0, 32, 128, 0, 160, 128, 0, 32, 0, 128,
#     160, 0, 128, 32, 128, 128, 160, 128, 128, 96, 0, 0, 224, 0, 0, 96, 128, 0,
#     224, 128, 0, 96, 0, 128, 224, 0, 128, 96, 128, 128, 224, 128, 128, 32, 64,
#     0, 160, 64, 0, 32, 192, 0, 160, 192, 0, 32, 64, 128, 160, 64, 128, 32, 192,
#     128, 160, 192, 128, 96, 64, 0, 224, 64, 0, 96, 192, 0, 224, 192, 0, 96, 64,
#     128, 224, 64, 128, 96, 192, 128, 224, 192, 128, 32, 0, 64, 160, 0, 64, 32,
#     128, 64, 160, 128, 64, 32, 0, 192, 160, 0, 192, 32, 128, 192, 160, 128,
#     192, 96, 0, 64, 224, 0, 64, 96, 128, 64, 224, 128, 64, 96, 0, 192, 224, 0,
#     192, 96, 128, 192, 224, 128, 192, 32, 64, 64, 160, 64, 64, 32, 192, 64,
#     160, 192, 64, 32, 64, 192, 160, 64, 192, 32, 192, 192, 160, 192, 192, 96,
#     64, 64, 224, 64, 64, 96, 192, 64, 224, 192, 64, 96, 64, 192, 224, 64, 192,
#     96, 192, 192, 224, 192, 192, 0, 32, 0, 128, 32, 0, 0, 160, 0, 128, 160, 0,
#     0, 32, 128, 128, 32, 128, 0, 160, 128, 128, 160, 128, 64, 32, 0, 192, 32,
#     0, 64, 160, 0, 192, 160, 0, 64, 32, 128, 192, 32, 128, 64, 160, 128, 192,
#     160, 128, 0, 96, 0, 128, 96, 0, 0, 224, 0, 128, 224, 0, 0, 96, 128, 128,
#     96, 128, 0, 224, 128, 128, 224, 128, 64, 96, 0, 192, 96, 0, 64, 224, 0,
#     192, 224, 0, 64, 96, 128, 192, 96, 128, 64, 224, 128, 192, 224, 128, 0, 32,
#     64, 128, 32, 64, 0, 160, 64, 128, 160, 64, 0, 32, 192, 128, 32, 192, 0,
#     160, 192, 128, 160, 192, 64, 32, 64, 192, 32, 64, 64, 160, 64, 192, 160,
#     64, 64, 32, 192, 192, 32, 192, 64, 160, 192, 192, 160, 192, 0, 96, 64, 128,
#     96, 64, 0, 224, 64, 128, 224, 64, 0, 96, 192, 128, 96, 192, 0, 224, 192,
#     128, 224, 192, 64, 96, 64, 192, 96, 64, 64, 224, 64, 192, 224, 64, 64, 96,
#     192, 192, 96, 192, 64, 224, 192, 192, 224, 192, 32, 32, 0, 160, 32, 0, 32,
#     160, 0, 160, 160, 0, 32, 32, 128, 160, 32, 128, 32, 160, 128, 160, 160,
#     128, 96, 32, 0, 224, 32, 0, 96, 160, 0, 224, 160, 0, 96, 32, 128, 224, 32,
#     128, 96, 160, 128, 224, 160, 128, 32, 96, 0, 160, 96, 0, 32, 224, 0, 160,
#     224, 0, 32, 96, 128, 160, 96, 128, 32, 224, 128, 160, 224, 128, 96, 96, 0,
#     224, 96, 0, 96, 224, 0, 224, 224, 0, 96, 96, 128, 224, 96, 128, 96, 224,
#     128, 224, 224, 128, 32, 32, 64, 160, 32, 64, 32, 160, 64, 160, 160, 64, 32,
#     32, 192, 160, 32, 192, 32, 160, 192, 160, 160, 192, 96, 32, 64, 224, 32,
#     64, 96, 160, 64, 224, 160, 64, 96, 32, 192, 224, 32, 192, 96, 160, 192,
#     224, 160, 192, 32, 96, 64, 160, 96, 64, 32, 224, 64, 160, 224, 64, 32, 96,
#     192, 160, 96, 192, 32, 224, 192, 160, 224, 192, 96, 96, 64, 224, 96, 64,
#     96, 224, 64, 224, 224, 64, 96, 96, 192, 224, 96, 192, 96, 224, 192, 0, 0, 0
# ]


# def colorize_mask(mask, palette):
#     zero_pad = 256 * 3 - len(palette)
#     for i in range(zero_pad):
#         palette.append(0)
#     new_mask = Image.fromarray(mask.astype(np.uint8)).convert('P')
#     new_mask.putpalette(palette)
#     return new_mask

# def _colorize(img, cmap, mask_zero=False):
#     vmin = np.min(img)
#     vmax = np.max(img)
#     mask = (img <= 0).squeeze()
#     cm = plt.get_cmap(cmap)
#     colored_image = cm(np.clip(img.squeeze(), vmin, vmax) / vmax)[:, :, :3]
#     # Use white if no depth is available (<= 0)
#     if mask_zero:
#         colored_image[mask, :] = [1, 1, 1]
#     return colored_image

# def load_gray_semantic_label_image(image_path):
#     # Load the grayscale semantic label image as a PIL image
#     gray_img = Image.open(image_path)
#     return np.array(gray_img)

# def save_colorized_image(image_array, output_path, palette=Cityscapes_palette):
#     # Colorize the grayscale image
#     colorized_img = colorize_mask(image_array, palette)

#     # Save the colorized image
#     colorized_img.save(output_path)


# # Usage example
# input_image_path = "/home/aghosh/Projects/2PCNet/Datasets/synthia/GT/LABELS/0000000_labelTrainIds.png"
# output_image_path = "colorized_semantic_map.png" # Update with your path

# # Load the grayscale label image
# gray_semantic_label = load_gray_semantic_label_image(input_image_path)

# # Save the colorized image
# save_colorized_image(gray_semantic_label, output_image_path)


# #import numpy as np
# # import cv2

# # # Define the mapping from class ID to RGB values
# # class_to_color = {
# #     0: [0, 0, 0], # void
# #     1: [70, 130, 180], # sky
# #     2: [70, 70, 70], # Building
# #     3: [128, 64, 128], # Road
# #     4: [244, 35, 232], # Sidewalk
# #     5: [64, 64, 128], # Fence
# #     6: [107, 142, 35], # Vegetation
# #     7: [153, 153, 153], # Pole
# #     8: [0, 0, 142], # Car
# #     9: [220, 220, 0], # Traffic sign
# #     10: [220, 20, 60], # Pedestrian
# #     11: [119, 11, 32], # Bicycle
# #     12: [0, 0, 230], # Motorcycle
# #     13: [250, 170, 160], # Parking-slot
# #     14: [128, 64, 64], # Road-work
# #     15: [250, 170, 30], # Traffic light
# #     16: [152, 251, 152], # Terrain
# #     17: [255, 0, 0], # Rider
# #     18: [0, 0, 70], # Truck
# #     19: [0, 60, 100], # Bus
# #     20: [0, 80, 100], # Train
# #     21: [102, 102, 156], # Wall
# #     22: [102, 102, 156] # Lanemarking
# # }

# # # Convert a grayscale map to a color map
# # demo_image = "/home/aghosh/Projects/2PCNet/Datasets/synthia/GT/LABELS/0000000_labelTrainIds.png"

# # # Load the grayscale semantic segmentation map
# # gray_seg_map = cv2.imread(demo_image, cv2.IMREAD_UNCHANGED)

# # print("gray_seg_map.shape: ", gray_seg_map.shape)

# # # # TODO: save gray_seg_map as txt
# # # np.savetxt("gray_seg_map.txt", gray_seg_map, fmt="%d")

# # # Create an empty color image with 3 channels
# # color_seg_map = np.zeros((gray_seg_map.shape[0], gray_seg_map.shape[1], 3), dtype=np.uint8)

# # # Apply the color mapping and convert RGB to BGR
# # for class_id, color in class_to_color.items():
# #     # # Reverse the RGB values to get BGR
# #     bgr_color = color[::-1]
# #     color_seg_map[gray_seg_map == class_id] = bgr_color
# #     # color_seg_map[gray_seg_map == class_id] = color

# # # Save or display the color segmentation map
# # cv2.imwrite('path_to_colored_sem_seg_map.png', color_seg_map)