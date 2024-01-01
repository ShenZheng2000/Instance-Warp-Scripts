import torch

# old code: bad efficiency
# def make_symmetric_around_max(saliency_map): # size: (1, 2, 7)

#     # Find the column (axis) with the max value in the entire saliency_map
#     _, _, max_x = torch.where(saliency_map == saliency_map.max())
#     max_x = max_x[0].item()

#     # For each row in saliency_map
#     for batch in saliency_map:
#         for row in batch:
#             left_idx = max_x - 1
#             right_idx = max_x + 1

#             while left_idx >= 0 and right_idx < saliency_map.size(2):
#                 max_val = max(row[left_idx].item(), row[right_idx].item())
#                 row[left_idx] = max_val
#                 row[right_idx] = max_val
#                 left_idx -= 1
#                 right_idx += 1

#     return saliency_map

# new code: better efficiency
def make_symmetric_around_max(saliency_map):
    # Find the column (axis) with the max value in the entire saliency_map
    _, _, max_x = torch.where(saliency_map == saliency_map.max())
    max_x = max_x[0].item()

    # Define the range to iterate over for both left and right
    left_indices = torch.arange(max_x, -1, -1)
    right_indices = torch.arange(max_x, saliency_map.size(2))

    # Ensure the lengths of left_indices and right_indices are the same
    length = min(len(left_indices), len(right_indices))
    left_indices = left_indices[:length]
    right_indices = right_indices[:length]

    # Use broadcasting to find the max values between left and right for all rows
    max_values = torch.max(saliency_map[:, :, left_indices], saliency_map[:, :, right_indices])

    # Assign the max values to both sides of the matrix
    saliency_map[:, :, left_indices] = max_values
    saliency_map[:, :, right_indices] = max_values

    return saliency_map

# Create a toy example
saliency_map = torch.tensor([[
    [1, 1, 5, 1, 2, 3],
    [2, 3, 5, 6, 5, 4],
]])
# print("saliency_map shape", saliency_map.shape)
print("init", saliency_map[0])

# Apply the symmetry function
symmetric_saliency = make_symmetric_around_max(saliency_map)
print("final", symmetric_saliency[0])