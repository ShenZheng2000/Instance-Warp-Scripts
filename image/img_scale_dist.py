import json
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Purpose: Plot the histogram of bounding box areas, and visualize the area thresholds

dataset = sys.argv[1]

if dataset == 'synthia':
    det_file = "/home/aghosh/Projects/2PCNet/Datasets/synthia_seg2det_gt.json"
elif dataset == 'gta':
    det_file = "/home/aghosh/Projects/2PCNet/Datasets/gta_seg2det.json" # TODO: debug this
elif dataset == 'cityscapes':
    det_file = "/home/aghosh/Projects/2PCNet/Datasets/cityscapes_seg2det.json"
else:
    print("dataset not found")
    exit(0)

def plot_histogram(data1, label1, num_bins=50, output_path=''):

    # Calculate the min and max values for the x-axis
    min_val = data1.min()
    max_val = data1.max()

    # Define the bin edges for logarithmic scale
    bin_edges = np.logspace(np.log10(min_val), np.log10(max_val), num_bins)

    # Plot the histograms
    plt.hist(data1, bins=bin_edges, label=label1, color="#fb8072", alpha=0.95, density=False)

    # # Add vertical dotted lines at 32^2 and 96^2 for small and medium size thresholds
    plt.axvline(x=32**2, color='#984ea3', linestyle='--', linewidth=4, label='Small/Medium thres')
    plt.axvline(x=96**2, color='#f781bf', linestyle='--', linewidth=4, label='Medium/Large thres')

    plt.legend(loc='upper right', fontsize='large')
    plt.xlabel('Area', fontsize=20)
    # plt.ylabel('Frequency', fontsize=20)
    plt.ylabel('Density', fontsize=20)
    plt.xscale('log')
    plt.xlim(min_val, max_val)  # Set the x-axis limits
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.tight_layout()
    plt.savefig(output_path)

    print("saveed to ", output_path)

    plt.close()


# Read the JSON file
with open(det_file, 'r') as file:
    data = json.load(file)

# Initialize counters for small, medium, and large instances
small_count = 0
medium_count = 0
large_count = 0

# Define area thresholds
small_threshold = 32 * 32
medium_threshold = 96 * 96

# Lists to store areas for histogram
all_areas = []

# Iterate through the dictionary
for filename, bbox_list in data.items():
    for bbox in bbox_list:

        # skip if bbox is empty
        if len(bbox) == 0:
            print(f"filename = {filename}; bbox is {bbox}")
            continue

        # Calculate the area of the bounding box
        x1, y1, x2, y2 = bbox
        area = (x2 - x1) * (y2 - y1)

        # for non-positive area: skip
        if area <= 0:
            continue

        # Determine if it's small, medium, or large
        if area <= small_threshold:
            small_count += 1
        elif small_threshold < area <= medium_threshold:
            medium_count += 1
        else:
            large_count += 1
        
        # Append the area to the all_areas list
        all_areas.append(area)

# Convert the all_areas list to a NumPy array
all_areas = np.array(all_areas)

# Calculate percentages
total_instances = small_count + medium_count + large_count
small_percentage = (small_count / total_instances) * 100
medium_percentage = (medium_count / total_instances) * 100
large_percentage = (large_count / total_instances) * 100

print(f'Small Instances Percentage: {small_percentage:.2f}%'
      f'\nMedium Instances Percentage: {medium_percentage:.2f}%'
      f'\nLarge Instances Percentage: {large_percentage:.2f}%')

# Save histogram
plot_histogram(all_areas, 'All', output_path=f'hist_{dataset}.png')


# # For synthia
# Small Instances Percentage: 81.07%
# Medium Instances Percentage: 16.11%
# Large Instances Percentage: 2.82%

# For GTA
# Small Instances Percentage: 88.37%
# Medium Instances Percentage: 8.35%
# Large Instances Percentage: 3.27%


# For Cityscapes
# Small Instances Percentage: 50.68%
# Medium Instances Percentage: 32.89%
# Large Instances Percentage: 16.43%