# Purpose: get (A&B) and (A&!B) from A and B

# File paths
night_dataset = 'val/rainy.txt'
clear_dataset = 'val/daytime.txt'
clear_night_dataset = 'val/rainy_day.txt'
bad_night_dataset = 'val/rainy_night.txt'

# Read image filenames from night.txt and clear.txt
with open(night_dataset, 'r') as file:
    night_images = set(line.strip() for line in file)

with open(clear_dataset, 'r') as file:
    clear_images = set(line.strip() for line in file)

# Find images in both night.txt and clear.txt
clear_night_images = night_images.intersection(clear_images)

# Find images only in night.txt but not in clear.txt
bad_night_images = night_images - clear_images

print("len(clear_night_images): ", len(clear_night_images))
print("len(bad_night_images): ", len(bad_night_images))

# Write common images to clear_night.txt
with open(clear_night_dataset, 'w') as file:
    file.write('\n'.join(clear_night_images))

# Write night-only images to bad_night.txt
with open(bad_night_dataset, 'w') as file:
    file.write('\n'.join(bad_night_images))