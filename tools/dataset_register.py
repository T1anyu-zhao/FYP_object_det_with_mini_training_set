from detectron2.data.datasets import register_coco_instances

# register_coco_instances("coco_cub200_train", {}, "DeViT/devit/datasets/CUB_200_2011/annotations/cub200_coco_train.json", "DeViT/devit/datasets/CUB_200_2011/images")    
# register_coco_instances("coco_cub200_val", {}, "DeViT/devit/datasets/CUB_200_2011/annotations/cub200_coco_val.json", "DeViT/devit/datasets/CUB_200_2011/images")    

from detectron2.data import DatasetCatalog

# List all registered datasets
print("Registered datasets:", DatasetCatalog.list())

# Check if 'coco_cub200_train' is in the list
if "coco_cub200_train" in DatasetCatalog.list():
    print("'coco_cub200_train' is registered.")
else:
    print("'coco_cub200_train' is not registered.")
