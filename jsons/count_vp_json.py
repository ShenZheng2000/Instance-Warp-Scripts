import json

def count_vanishing_points_status(data, image_width, image_height):
    both_oob_count = 0
    one_oob_count = 0
    none_oob_count = 0

    for vanishing_point in data.values():
        x, y = vanishing_point
        if (0 <= x < image_width) and (0 <= y < image_height):
            none_oob_count += 1
        elif not (0 <= x < image_width) and not (0 <= y < image_height):
            both_oob_count += 1
        else:
            one_oob_count += 1

    return both_oob_count, one_oob_count, none_oob_count

def main():
    # file_path = "/home/aghosh/Projects/2PCNet/Datasets/cityscapes/combined_filtered_images_vps.json"  # Replace this with the actual file path
    # file_path = "/home/aghosh/Projects/2PCNet/Datasets/VP/acdc_all_vp.json"
    file_path = "/home/aghosh/Projects/2PCNet/Datasets/VP/synthia_all_vp.json"
    # image_width = 1280
    # image_height = 720
    # image_width = 2048
    # image_height = 1024
    # image_width = 1920
    # image_height = 1080
    image_width = 720
    image_height = 960

    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    # Count vanishing point status
    both_oob, one_oob, none_oob = count_vanishing_points_status(data, image_width, image_height)

    print("Vanishing points with both coordinates out of bounds:", both_oob) # some for BDD and synthia, none for cityscapes, dark zurich, acdc
    print("Vanishing points with one coordinate out of bounds:", one_oob)
    print("Vanishing points with none of the coordinates out of bounds:", none_oob)

if __name__ == "__main__":
    main()