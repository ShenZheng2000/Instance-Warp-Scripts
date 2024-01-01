import cv2
import os

# NOTE: be carefully! Will save in current directory!!!!

# # Define the root folder containing subfolders with images
# root_folder = "/home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/bdd100k_10_18_baseline/gm_rainy_day/inference/visual"
# root_folder = "/home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/bdd100k_10_18_bbox/gm_rainy_day/inference/visual"\

# root_folder = "/home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/bdd100k_10_18_baseline/gm_rainy_night/inference/visual"
# root_folder = "/home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/bdd100k_10_18_bbox/gm_rainy_night/inference/visual"

# root_folder = "/home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/dense_foggy_12_12_baseline/gm_foggy_day/inference/visual"
root_folder = "/home/aghosh/Projects/2PCNet/Methods/Instance-Warp/Night-Object-Detection/outputs/dense_foggy_12_12_bbox/gm_foggy_day/inference/visual"

# Get a list of all subfolders in the root folder
# subfolders = [f for f in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, f))]
# subfolders = [f.path for f in os.scandir(root_folder) if f.is_dir()]
# print("subfolders =", subfolders)

# Define the codec for the video (e.g., XVID for .avi or H.264 for .mp4)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

for subdir, dirs, files in os.walk(root_folder):

    # Filter out image files
    image_files = [os.path.join(subdir, file) for file in files if file.lower().endswith(('.jpg', '.png'))]
    
    # Skip the loop iteration if no images found in the current subdir
    if not image_files:
        continue

    # Sort the image files based on their names
    image_files.sort()
    
    # Get the resolution of the first image
    first_image = cv2.imread(image_files[0])
    height, width, layers = first_image.shape

    # Get the name of the subfolder
    subfolder_name = os.path.basename(subdir)

    # Define the output video file path for the subfolder
    output_video_path = os.path.join(root_folder, f"{subfolder_name}.mp4")

    # print("output_video_path is", output_video_path)
    # exit()

    # Create a VideoWriter object for the subfolder
    out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (width, height))

    for image_file in image_files:
        # Read the image
        img = cv2.imread(image_file)

        # Write the image to the video
        out.write(img)

    # Release the VideoWriter object
    out.release()

    print(f"Video saved to {output_video_path}")

print("All videos processed.")