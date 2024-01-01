from pycocotools.coco import COCO

# COCO JSON文件的路径
coco_json_file = '/home/aghosh/Projects/2PCNet/Datasets/cityscapes/gt_detection/instancesonly_filtered_gtFine_train_poly.json'

# 创建COCO对象
coco = COCO(coco_json_file)

# 获取图像ID列表
image_ids = coco.getImgIds()

# 计算图像数量
num_images = len(image_ids)

# 打印图像数量
print("COCO JSON文件中的图像数量:", num_images)
