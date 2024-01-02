import os
from collections import Counter

# BDD100K categories
# {
#     "categories": [
#         {
#             "id": 1,
#             "name": "pedestrian"
#         },
#         {
#             "id": 2,
#             "name": "rider"
#         },
#         {
#             "id": 3,
#             "name": "car"
#         },
#         {
#             "id": 4,
#             "name": "truck"
#         },
#         {
#             "id": 5,
#             "name": "bus"
#         },
#         {
#             "id": 6,
#             "name": "train"
#         },
#         {
#             "id": 7,
#             "name": "motorcycle"
#         },
#         {
#             "id": 8,
#             "name": "bicycle"
#         },
#         {
#             "id": 9,
#             "name": "traffic light"
#         },
#         {
#             "id": 10,
#             "name": "traffic sign"
#         }
#     ]
# }

# NOTE: Convert mapping for these
# ['PassengerCar', 'Vehicle_is_group', 'PassengerCar_is_group', 'Vehicle']: id: 3 => car
# ['LargeVehicle', 'LargeVehicle_is_group']: id: 5 => bus
# ['Pedestrian', 'person', 'Pedestrian_is_group']: id: 1 => pedestrian
# ['RidableVehicle', 'RidableVehicle_is_group']: id: 8 => bicycle

# NOTE: skip this
# 'Obstacle': 2343
# 'DontCare': 5296
# 'train': 1



def count_categories_in_txt_files(folder_path):
    category_counts = Counter()

    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'r') as f:
                for line in f:
                    words = line.strip().split()
                    if words:
                        category = words[0]
                        category_counts[category] += 1

    return category_counts

# Replace 'your_folder_path' with the path to your folder containing the text files
folder_path = '/longdata/anurag_storage/DENSE/gt_labels/cam_left_labels_TMP'
counts = count_categories_in_txt_files(folder_path)

for category, count in counts.items():
    print(f"'{category}': {count}")

