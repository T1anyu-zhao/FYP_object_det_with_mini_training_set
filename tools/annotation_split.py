import json
import os
from PIL import Image

dataset_dir = '/rds/general/user/az2120/home/DeViT/devit/datasets/CUB_200_2011'
images_dir = os.path.join(dataset_dir, 'images')
class_labels_path = os.path.join(dataset_dir, 'image_class_labels.txt')
classes_info_path = os.path.join(dataset_dir, 'classes.txt')

# Paths to files
coco_json_path = os.path.join(dataset_dir, 'annotations/cub200_coco_format.json')
split_txt_path = os.path.join(dataset_dir, 'train_test_split.txt')
train_json_path = os.path.join(dataset_dir, 'annotations/cub200_coco_train.json')
val_json_path = os.path.join(dataset_dir, 'annotations/cub200_coco_val.json')

# Load the COCO annotations
with open(coco_json_path, 'r') as f:
    coco_data = json.load(f)

# Load the split information
with open(split_txt_path, 'r') as f:
    split_info = f.readlines()

# Parse the split information
split_dict = {}
for line in split_info:
    image_id, split_label = line.strip().split()
    split_dict[int(image_id)] = int(split_label)

info = {
    "description": "The Caltech-UCSD Birds-200-2011 Dataset",
    "url": "http://www.vision.caltech.edu/visipedia/CUB-200-2011.html",
    "version": "1.0",
    "year": 2011,
    "contributor": "C. Wah, S. Branson, P. Welinder, P. Perona, S. Belongie",
    "date_created": "2011/06/11",
    "institution": "California Institute of Technology",
    "number": "CNS-TR-2011-001"
}

# Initialize new dictionaries for training and validation
train_data = {
    'info':info,
    'images': [],
    'annotations': [],
    'categories': coco_data.get('categories', [])
}
val_data = {
    'info':info,
    'images': [],
    'annotations': [],
    'categories': coco_data.get('categories', [])
}

# Separate images and annotations into training and validation
for image in coco_data['images']:
    image_id = image['id']
    if split_dict[image_id] == 0:
        val_data['images'].append(image)
    else:
        train_data['images'].append(image)

# Create a lookup for image ids to split annotations
train_image_ids = {img['id'] for img in train_data['images']}
val_image_ids = {img['id'] for img in val_data['images']}

# Split annotations based on image id
for annotation in coco_data['annotations']:
    if annotation['image_id'] in train_image_ids:
        train_data['annotations'].append(annotation)
    elif annotation['image_id'] in val_image_ids:
        val_data['annotations'].append(annotation)

# Save the new JSON files
with open(train_json_path, 'w') as f:
    json.dump(train_data, f, indent=2)

with open(val_json_path, 'w') as f:
    json.dump(val_data, f, indent=2)

print(f"Training data saved to {train_json_path}")
print(f"Validation data saved to {val_json_path}")
