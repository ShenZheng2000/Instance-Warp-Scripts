import json
from collections import defaultdict
from tabulate import tabulate

# Purpose: count the number of instances per category in a COCO format JSON file

# Load the COCO format JSON file
# coco_json_file = '/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/bdd100k_labels_images_train.json'
coco_json_file = '/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/bdd100k_labels_images_val.json'
with open(coco_json_file, 'r') as file:
    coco_data = json.load(file)

# Create a dictionary to store category-wise instance counts
category_counts = defaultdict(int)

# Iterate through annotations and count instances per category
for annotation in coco_data['annotations']:
    category_id = annotation['category_id']
    category_counts[category_id] += 1

# Load the COCO categories to get category names
categories = coco_data['categories']
category_id_to_name = {category['id']: category['name'] for category in categories}

# Calculate the total number of instances
total_instances = sum(category_counts.values())

# Create a list to store the results
results = []

# Calculate the percentage for each category and add it to the results
for category_id, count in category_counts.items():
    category_name = category_id_to_name[category_id]
    percentage = (count / total_instances) * 100
    results.append([category_name, count, f"{percentage:.2f}%"])

# Sort the results by category name
results.sort(key=lambda x: x[0])

# Print the results as a table
table_headers = ["Category", "Instances", "Percentage"]
table = tabulate(results, headers=table_headers, tablefmt="grid")
print(table)


# This is the stat for training images
# +---------------+-------------+--------------+
# | Category      |   Instances | Percentage   |
# +===============+=============+==============+
# | bicycle       |        7210 | 0.56%        |  => small percent
# +---------------+-------------+--------------+
# | bus           |       11672 | 0.91%        |  => small percent
# +---------------+-------------+--------------+
# | car           |      713211 | 55.42%       |
# +---------------+-------------+--------------+
# | motorcycle    |        3002 | 0.23%        | => small percent
# +---------------+-------------+--------------+
# | person        |       95866 | 7.45%        |
# +---------------+-------------+--------------+
# | stop sign     |      239686 | 18.63%       |
# +---------------+-------------+--------------+
# | traffic light |      186117 | 14.46%       |
# +---------------+-------------+--------------+
# | train         |         136 | 0.01%        |  => very small percent (not evaluated so it is OK)
# +---------------+-------------+--------------+
# | truck         |       29971 | 2.33%        |
# +---------------+-------------+--------------+


# This is the stat for testing images
# +---------------+-------------+--------------+
# | Category      |   Instances | Percentage   |
# +===============+=============+==============+
# | bicycle       |        1007 | 0.54%        |
# +---------------+-------------+--------------+
# | bus           |        1597 | 0.86%        |
# +---------------+-------------+--------------+
# | car           |      102506 | 55.25%       |
# +---------------+-------------+--------------+
# | motorcycle    |         452 | 0.24%        |
# +---------------+-------------+--------------+
# | person        |       13911 | 7.50%        |
# +---------------+-------------+--------------+
# | stop sign     |       34908 | 18.82%       |
# +---------------+-------------+--------------+
# | traffic light |       26885 | 14.49%       |
# +---------------+-------------+--------------+
# | train         |          15 | 0.01%        |
# +---------------+-------------+--------------+
# | truck         |        4245 | 2.29%        |
# +---------------+-------------+--------------+