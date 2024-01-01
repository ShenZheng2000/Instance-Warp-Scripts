import cv2
import os

# base_folder = '/home/aghosh/Projects/2PCNet/Datasets/gm/rainy/day'
# base_folder = '/home/aghosh/Projects/2PCNet/Datasets/gm/rainy/night'
base_folder = '/home/aghosh/Projects/2PCNet/Datasets/gm/foggy/day'

# Define the path to the folder containing your MP4 files
input_folder = f'{base_folder}/videos'

# Create an output folder where the frames from each video will be saved
output_root_folder = f'{base_folder}/images'
os.makedirs(output_root_folder, exist_ok=True)

# List all MP4 files in the input folder
mp4_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.mp4')]

for mp4_file in mp4_files:
    # Construct the full path to the MP4 file
    video_path = os.path.join(input_folder, mp4_file)

    # Create a folder for the frames of this video
    video_name = os.path.splitext(mp4_file)[0]
    output_directory = os.path.join(output_root_folder, video_name)
    os.makedirs(output_directory, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Initialize frame counter
    frame_count = 0

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # Break the loop if we've reached the end of the video
        if not ret:
            break

        # Save the frame as an image
        frame_filename = os.path.join(output_directory, f'frame_{frame_count:04d}.jpg')
        cv2.imwrite(frame_filename, frame)

        # Increment the frame counter
        frame_count += 1

    # Release the video capture object
    cap.release()

    print(f"Extracted {frame_count} frames from {mp4_file} to {output_directory}")

print("All videos processed.")
