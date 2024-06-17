import json
import os
from PIL import Image

# Paths to the dataset files
dataset_dir = '/rds/general/user/az2120/home/DeViT/devit/datasets/CUB_200_2011'
images_dir = os.path.join(dataset_dir, 'images')
images_info_path = os.path.join(dataset_dir, 'images.txt')
bounding_boxes_path = os.path.join(dataset_dir, 'bounding_boxes.txt')
class_labels_path = os.path.join(dataset_dir, 'image_class_labels.txt')
classes_info_path = os.path.join(dataset_dir, 'classes.txt')

# Read class information
class_id_to_name = {}
with open(classes_info_path, 'r') as file:
    for line in file:
        class_id, class_name = line.strip().split(' ', 1)
        class_id_to_name[int(class_id)] = class_name

print("class id name matching done")

# COCO dataset structure
coco_data = {
    "images": [],
    "annotations": [],
    "categories": []
}

# Add category information
for class_id, class_name in class_id_to_name.items():
    coco_data['categories'].append({
        "id": class_id,
        "name": class_name
    })

print("categories loading done")

# Helper dictionaries
image_id_to_file = {}
with open(images_info_path, 'r') as file:
    for line in file:
        image_id, image_file = line.strip().split(' ', 1)
        image_id_to_file[int(image_id)] = image_file

print("file path matched")

# Read bounding box information
with open(bounding_boxes_path, 'r') as file:
    for line in file:
        image_id, x, y, width, height = map(float, line.strip().split())
        image_id = int(image_id)
        file_name = image_id_to_file[image_id]
        file_path = os.path.join(images_dir, file_name)
        
        # Image details
        with Image.open(file_path) as img:
            width_i, height_i = img.size
        coco_data['images'].append({
            "id": image_id,
            "width": width_i,
            "height": height_i,
            "file_name": file_name
        })

        # Annotation details
        coco_data['annotations'].append({
            "id": len(coco_data['annotations']) + 1,
            "image_id": image_id,
            "category_id": int(next(open(class_labels_path)).split()[1]),
            "bbox": [x, y, width, height],
            "area": width * height,
            "iscrowd": 0
        })

print("annotation done")
# Output file
with open('cub200_coco_format.json', 'w') as f:
    json.dump(coco_data, f)

print("Conversion complete. Output file created: 'cub200_coco_format.json'")
