import json

# Load the JSON file
json_file_path = "/home/aghosh/Projects/2PCNet/Datasets/VP/train_day.json"  # Replace with the actual path to your JSON file
with open(json_file_path, 'r') as json_file:
    vanishing_points = json.load(json_file)

# Initialize variables to store the sum of widths and heights
total_width = 0
total_height = 0

# Iterate through the vanishing points and calculate the sum of widths and heights
for image_path, vp in vanishing_points.items():
    total_width += vp[0]  # Add the width (first element) to the total_width
    total_height += vp[1]  # Add the height (second element) to the total_height

# Calculate the average width and average height
num_images = len(vanishing_points)
average_width = total_width / num_images
average_height = total_height / num_images

print(f"Average Width: {average_width:.3f}")
print(f"Average Height: {average_height:.3f}")

print(f"Average Width Ratio: {average_width / 1280:.3f}")
print(f"Average Height Ratio: {average_height / 720:.3f}")
