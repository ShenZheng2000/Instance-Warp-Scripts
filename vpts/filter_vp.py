# import os
# import json

# # Define the paths
# json_file_path = "/home/aghosh/Projects/2PCNet/Datasets/VP/bdd100k_all_vp.json"
# image_folder_path = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/100k/train_day"

# # Load the JSON data
# with open(json_file_path, 'r') as json_file:
#     data = json.load(json_file)

# # Extract basenames of all images in the folder
# image_basenames = {os.path.basename(image) for image in os.listdir(image_folder_path) \
#                    if image.endswith(('.jpg', '.png'))}  # Adjust the extensions if needed

# # Filter the JSON data
# filtered_data = {key: value for key, value in data.items() if os.path.basename(key) in image_basenames}

# # Save the filtered data
# output_file_path = "/home/aghosh/Projects/2PCNet/Datasets/VP/train_day.json"
# with open(output_file_path, 'w') as output_file:
#     json.dump(filtered_data, output_file)

# print(f"Filtered JSON saved to {output_file_path}")
