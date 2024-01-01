# total_dataset = 'val/daytime.txt'
# sub_dataset = 'val/clear.txt'
# total_sub_dataset = 'val/daytime_good_weather.txt'
# total_no_sub_dataset = 'val/daytime_bad_weather.txt'

# total_dataset = 'val/clear.txt'
# sub_dataset = 'val/night.txt'
# common_dataset = 'val/clear_night.txt'
# uncommon_dataset = 'val/clear_no_night.txt'

# # Read image filenames from daytime.txt and clear.txt
# with open(total_dataset, 'r') as daytime_file:
#     total_images = set(line.strip() for line in daytime_file)

# with open(sub_dataset, 'r') as clear_file:
#     sub_images = set(line.strip() for line in clear_file)

# # Find images in both daytime.txt and clear.txt
# common_images = total_images.intersection(sub_images)

# # Find images only in daytime.txt
# uncommon_images = total_images - sub_images

# # print(len(total_images))
# # print(len(sub_images))
# # print(len(common_images))
# # print(len(uncommon_images))
# # exit()

# # TODO: think: is particly cloudy and overcast weather good or bad?

# # Write common images to daytime_good_weather.txt
# with open(common_dataset, 'w') as good_weather_file:
#     good_weather_file.write('\n'.join(common_images))

# # Write daytime-only images to daytime_bad_weather.txt
# with open(uncommon_dataset, 'w') as bad_weather_file:
#     bad_weather_file.write('\n'.join(uncommon_images))

# TODO: now we want rainy -> (rainy day and rainy night)

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