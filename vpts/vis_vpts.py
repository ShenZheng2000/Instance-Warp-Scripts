import json
import numpy as np
import cv2
from sklearn.cluster import KMeans

# Purpose: Visualize vanishing points and calculate statistics

def read_vanishing_points(file_path):
    with open(file_path, "r") as f:
        vanishing_points_data = json.load(f)
    return vanishing_points_data

def create_canvas(height, width):
    return np.ones((height, width, 3), dtype=np.uint8) * 255  # White background

def plot_vanishing_points(canvas, points, center_height, center_width, radius=1):
    x_coordinates = []
    y_coordinates = []
    
    for image_path, (x, y) in points.items():
        x = int(x)
        y = int(y)

        if 0 <= x < canvas.shape[1] and 0 <= y < canvas.shape[0]:
            cv2.circle(canvas, (x, y), radius, (0, 0, 255), -1)
            x_coordinates.append(x - center_width)
            y_coordinates.append(y - center_height)
    
    return canvas, x_coordinates, y_coordinates

def calculate_statistics(x_coords, y_coords):
    mean_x = np.mean(x_coords)
    std_x = np.std(x_coords)
    mean_y = np.mean(y_coords)
    std_y = np.std(y_coords)
    return mean_x, std_x, mean_y, std_y

def perform_kmeans_clustering(data):
    kmeans = KMeans()
    kmeans.fit(data)
    cluster_labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_
    return cluster_labels, cluster_centers

def main():
    # Define canvas dimensions (height and width)
    canvas_height = 720
    canvas_width = 1280
    center_height = canvas_height // 2
    center_width = canvas_width // 2

    # Load vanishing points data
    vanishing_points_data = read_vanishing_points("/home/aghosh/Projects/2PCNet/Datasets/VP/train_day.json")

    # Create a canvas with a white background
    combined_canvas = create_canvas(canvas_height, canvas_width)

    # Plot vanishing points on the canvas and get coordinates
    combined_canvas, x_coordinates, y_coordinates = plot_vanishing_points(
        combined_canvas, vanishing_points_data, center_height, center_width
    )

    # Save the combined canvas as an image file (e.g., PNG)
    cv2.imwrite("combined_vanishing_points.png", combined_canvas)

    # Calculate statistics for x and y coordinates
    mean_x, std_x, mean_y, std_y = calculate_statistics(x_coordinates, y_coordinates)

    # Print statistics in a table format
    table_format = "{:<30} | {:<10}"
    print("-" * 45)
    print(table_format.format("Statistic", "Relative Value"))
    print("-" * 45)
    print(table_format.format("Mean X Coordinate", f"{mean_x:.2f}"))
    print(table_format.format("Std. Deviation X Coordinate", f"{std_x:.2f}"))
    print(table_format.format("Mean Y Coordinate", f"{mean_y:.2f}"))
    print(table_format.format("Std. Deviation Y Coordinate", f"{std_y:.2f}"))
    print("-" * 45)

    # Perform K-means clustering with default k value
    data = np.array(list(zip(x_coordinates, y_coordinates)))
    cluster_labels, cluster_centers = perform_kmeans_clustering(data)

    # # Print the cluster labels for each point
    # print("Cluster Labels:")
    # print(cluster_labels)

    # # Print the cluster centers
    # print("Cluster Centers:")
    # print(cluster_centers)

    # Add cluster centers to the original image
    for center in cluster_centers:
        x_center, y_center = center.astype(int)
        cv2.circle(combined_canvas, (x_center + center_width, y_center + center_height), 10, (0, 0, 0), -1)  # Green color

    # Save the updated canvas with cluster centers as an image file
    cv2.imwrite("combined_vanishing_points_with_centers.png", combined_canvas)

if __name__ == "__main__":
    main()
