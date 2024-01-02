# Purpose: split bdd images based on weather and time of day

import json
from collections import defaultdict
import os

train_file = '/home/aghosh/Projects/2PCNet/Datasets/bdd100k_ori/labels/det_20/det_train.json'
val_file = "/home/aghosh/Projects/2PCNet/Datasets/bdd100k_ori/labels/det_20/det_val.json"

def process_json(json_file, folder):
    # Ensure the folder exists
    if not os.path.exists(folder):
        os.mkdir(folder)

    # Step 1: Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Use defaultdicts to store names based on conditions
    weathers = defaultdict(list)
    times_of_day = defaultdict(list)

    # Step 2: Dynamically extract and categorize the entries
    for entry in data:
        weather = entry['attributes']['weather']
        time_of_day = entry['attributes']['timeofday']

        # Categorize based on weather
        weathers[weather].append(entry['name'])

        # If time_of_day is not 'daytime', categorize as 'night'
        if time_of_day == 'undefined':
            times_of_day['undefined'].append(entry['name'])
        elif time_of_day == 'daytime':
            times_of_day['daytime'].append(entry['name'])
        else:
            times_of_day['night'].append(entry['name'])

    # Step 3: Write the names to separate `.txt` files based on weather
    for weather_file, names in weathers.items():
        with open(os.path.join(folder, f"{weather_file}.txt"), 'w') as file:
            for name in names:
                file.write(name + '\n')

    # Step 4: Write the names to separate `.txt` files based on time of day
    for time_file, names in times_of_day.items():
        with open(os.path.join(folder, f"{time_file}.txt"), 'w') as file:
            for name in names:
                file.write(name + '\n')

if __name__ == '__main__':
    process_json(train_file, 'train')
    process_json(val_file, 'val')
