import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
import statistics
from tabulate import tabulate

def process_annotations(data, files, sizes_list, confidences_list, id_to_file):
    for annotation in data['annotations']:
        file_name = id_to_file[annotation['image_id']]
        if file_name in files:
            bbox = annotation['bbox']
            sizes_list.append((bbox[2], bbox[3]))
            if 'score' in annotation:  # Check if 'score' exists before using it
                confidence = annotation['score']
                confidences_list.append(confidence)

def plot_sizes(ax, sizes_list, cmap, gridsize=30, mincnt=1, alpha=0.8):
    if sizes_list:
        x, y = zip(*sizes_list)  # unpack the width and height pairs
        hb = ax.hexbin(x, y, gridsize=gridsize, cmap=cmap, mincnt=mincnt, alpha=alpha, norm=LogNorm())
        cb = plt.colorbar(hb, ax=ax)
        cb.set_label('counts')

def plot_confidence(ax, confidences_list, color):
    if confidences_list:
        weights = np.ones_like(confidences_list) / len(confidences_list)  # Create weights for each confidence value
        ax.hist(confidences_list, bins=20, color=color, alpha=0.7, weights=weights)  # Pass weights to the hist function
        ax.set_ylim(0, 1)  # Optional: limit y-axis values to be between 0 and 1

def load_files(file_path):
    with open(file_path) as f:
        return [file.strip() for file in f.readlines()]

def create_subplots(ax, title, xlabel, ylabel):
    ax.set_title(title, fontsize=16)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)

def calculate_mean(data, decimals=2):
    if isinstance(data[0], tuple):
        # Transpose the list of tuples to get separate lists for each element of the tuple
        transposed_data = list(zip(*data))
        
        # Calculate the mean and standard deviation for each element
        means = [round(statistics.mean(sublist), decimals) for sublist in transposed_data]
        return means
    else:
        mean = round(statistics.mean(data), decimals)
        return mean

def main():

    # Load the COCO annotations
    # src_json = '/home/aghosh/Projects/2PCNet/outputs/pretrained/inference/coco_instances_results_COCO.json'
    src_json = '/home/aghosh/Projects/2PCNet/Datasets/bdd100k/coco_labels/val_night.json'

    with open(src_json) as f:
        data = json.load(f)

    # Create a dictionary to map image_id to file_name
    id_to_file = {image['id']: image['file_name'] for image in data['images']}

    # Load the filenames for each time of day
    dusk_files = load_files('/home/aghosh/Projects/2PCNet/Scripts/jsons/txt_out_val/dawn_dusk_images.txt')
    night_files = load_files('/home/aghosh/Projects/2PCNet/Scripts/jsons/txt_out_val/night_images.txt')

    # Create lists to store the bbox sizes and confidence scores for each time of day
    dusk_sizes, dusk_confidences = [], []
    night_sizes, night_confidences = [], []

    # Process the annotations for dusk and night
    process_annotations(data, dusk_files, dusk_sizes, dusk_confidences, id_to_file)
    process_annotations(data, night_files, night_sizes, night_confidences, id_to_file)

    fig, axs = plt.subplots(2, 2, figsize=(18, 12))  # Four subplots

    # Plot the bbox sizes for each time of day
    plot_sizes(axs[0, 0], dusk_sizes, "Reds")
    create_subplots(axs[0, 0], 'Dusk Bbox Sizes', 'Width', 'Height')

    plot_sizes(axs[0, 1], night_sizes, "Blues")
    create_subplots(axs[0, 1], 'Night Bbox Sizes', 'Width', 'Height')

    # Plot the confidence scores for each time of day
    plot_confidence(axs[1, 0], dusk_confidences, "red")
    create_subplots(axs[1, 0], 'Dusk Confidence Scores', 'Confidence', 'Frequency')

    plot_confidence(axs[1, 1], night_confidences, "blue")
    create_subplots(axs[1, 1], 'Night Confidence Scores', 'Confidence', 'Frequency')

    plt.tight_layout()
    plt.savefig('sizes_and_confidences.png', dpi=300)  # Save the figure as a PNG file
    plt.show()

    table = []
    table.append(["Time", "Size (Width/Height)", "Confidence"])
    table.append(["Dusk", calculate_mean(dusk_sizes), calculate_mean(dusk_confidences) if dusk_confidences else None])
    table.append(["Night", calculate_mean(night_sizes), calculate_mean(night_confidences) if night_confidences else None])
    print(tabulate(table))

    print("================================================================>")
    print(f"Finished processing {len(data['annotations'])} objects")


if __name__ == '__main__':
    main()