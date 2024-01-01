import matplotlib.pyplot as plt
import torch

# Coordinates as tensors
points = [
    torch.tensor([[392.2950, 393.7193]]), # Top (red)
    torch.tensor([[775.9950, 415.8443]]), # Top (red)
    torch.tensor([[775.9950, 466.2669]]), # Bottom (blue)
    torch.tensor([[392.2950, 433.0441]])  # Bottom (blue)
]

# Load your image (replace 'your_image_path.jpg' with your actual image path)
image = plt.imread('/home/aghosh/Projects/2PCNet/Methods/Night-Object-Detection/twophase/data/transforms/triplet_layer_global.png')

# Create a Matplotlib figure and axis
fig, ax = plt.subplots()

# Display the image
ax.imshow(image)

# Plot the points on the image
for i, point in enumerate(points):
    x, y = point[0]
    color = 'red' if i < 2 else 'blue'
    ax.plot(x, y, 'o', color=color)  # Use 'o' marker and set color dynamically

# Show the image with points
plt.savefig('triplet_layer_global.png')
