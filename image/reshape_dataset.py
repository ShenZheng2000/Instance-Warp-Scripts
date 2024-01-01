import cv2
import os

def resize_images(source_directory, destination_directory, width=1280, height=720):
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    
    for image_name in os.listdir(source_directory):
        image_path = os.path.join(source_directory, image_name)
        img = cv2.imread(image_path)
        
        # Resize the image
        resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
        
        # Save the resized image to the destination directory
        dest_path = os.path.join(destination_directory, image_name)
        cv2.imwrite(dest_path, resized_img)

    print(f"Resized images saved to {destination_directory}")

# Example usage
source_dir = '/home/aghosh/Projects/2PCNet/LLIE/Results/SGZ/val_night_ori'
destination_dir = '/home/aghosh/Projects/2PCNet/LLIE/Results/SGZ/val_night'
resize_images(source_dir, destination_dir)