
image_width = 1024
image_height = 512

# List of bounding boxes
bboxes = [[ 255.0000,   22.0000,  291.0000,   87.5000],
        [ 987.5000,   40.0000, 1016.0000,  104.0000],
        [ 973.5000,   97.5000,  985.5000,  117.0000],
        [ 176.5000,  101.0000,  196.5000,  147.5000],
        [ 259.5000,  138.5000,  272.5000,  166.5000],
        [ 565.0000,  182.5000,  567.0000,  187.0000],
        [  49.5000,   35.5000,   56.0000,   66.5000],
        [  23.0000,   77.5000,   41.5000,  116.0000],
        [ 185.5000,   84.0000,  215.0000,   95.0000],
        [ 246.5000,   93.5000,  286.0000,  131.5000],
        [ 827.5000,  130.5000,  850.5000,  142.5000],
        [ 817.5000,  135.0000,  831.5000,  143.0000],
        [ 408.5000,  135.0000,  443.0000,  143.0000],
        [ 386.5000,  137.5000,  404.5000,  158.5000],
        [ 817.5000,  143.5000,  849.5000,  167.5000],
        [ 408.5000,  145.0000,  443.0000,  151.0000],
        [ 754.5000,  147.5000,  771.5000,  163.0000],
        [ 408.5000,  152.5000,  442.5000,  160.0000],
        [ 451.5000,  155.0000,  457.5000,  161.5000],
        [ 408.0000,  162.5000,  460.5000,  174.5000],
        [ 723.0000,  163.0000,  729.5000,  184.5000],
        [ 761.5000,  166.0000,  776.0000,  190.0000],
        [ 758.5000,  167.5000,  759.5000,  170.5000],
        [ 816.5000,  170.0000,  848.0000,  191.5000],
        [ 755.5000,  172.5000,  759.0000,  190.0000],
        [ 471.5000,  175.0000,  476.0000,  178.0000],
        [ 438.0000,  176.0000,  459.5000,  181.5000],
        [ 400.5000,  182.0000,  416.0000,  213.0000],
        [ 166.0000,  182.5000,  191.0000,  217.5000],
        [   3.0000,  133.0000,  170.5000,  399.0000],
        [ 446.0000,  178.5000,  514.5000,  236.5000],
        [ 567.0000,  182.0000,  637.5000,  229.5000],
        [ 663.0000,  189.0000,  711.5000,  225.5000],
        [ 759.5000,  190.5000,  910.5000,  243.5000],
        [ 641.0000,  195.5000,  655.0000,  223.5000],
        [ 541.0000,  195.0000,  567.0000,  212.5000],
        [ 521.5000,  195.0000,  539.0000,  213.0000],
        [ 635.5000,  197.0000,  639.0000,  207.5000],
        [ 754.0000,  200.5000,  757.5000,  223.5000],
        [ 732.5000,  202.5000,  739.0000,  213.5000],
        [ 668.5000,  205.5000,  670.5000,  208.5000],
        [ 664.0000,  205.5000,  664.0000,  207.0000],
        [ 671.0000,  207.0000,  676.0000,  225.0000],
        [ 990.5000,  143.5000, 1020.5000,  249.5000],
        [ 945.5000,  143.5000,  984.0000,  249.0000],
        [ 902.5000,  143.5000,  923.0000,  232.5000],
        [1019.0000,  154.0000, 1021.0000,  170.5000],
        [ 658.5000,  202.0000,  671.0000,  226.0000],
        [ 725.0000,  209.0000,  736.5000,  226.0000],
        [ 671.0000,  209.5000,  674.5000,  225.0000]]


# Function to check if a bounding box is out of bounds
def is_bbox_out_of_bounds(bbox, image_width, image_height):
    x1, y1, x2, y2 = bbox
    if x1 == x2 or y1 == y2:
        print("Found a bounding box with zero area.")
    return x1 < 0 or x2 > image_width or y1 < 0 or y2 > image_height

# Check if any bounding boxes are out of bounds
out_of_bounds = any(is_bbox_out_of_bounds(bbox, image_width, image_height) for bbox in bboxes)

if out_of_bounds:
    print("At least one bounding box is out of bounds.")
else:
    print("All bounding boxes are within bounds.")