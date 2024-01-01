import os

# Define the path to your folder of images and the output text file
image_folder = '/home/aghosh/Projects/2PCNet/Datasets/bdd100k/images/100k/Rainy_bad'
output_file = '/home/aghosh/Projects/2PCNet/Scripts/bdd/val/rainy_100.txt'

# Define the allowed image extensions
allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}

# Open the output file
with open(output_file, 'w') as file:
    # Iterate over the files in the image folder
    for image in os.listdir(image_folder):
        # Check if the file is an image
        if os.path.splitext(image)[1].lower() in allowed_extensions:
            # Write the basename of the image to the file
            file.write(image + '\n')

print(f"Image basenames written to {output_file}")
