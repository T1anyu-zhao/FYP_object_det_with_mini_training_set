from pycocotools.coco import COCO
import matplotlib.pyplot as plt
import skimage.io as io
import random
from pycocotools.coco import COCO
import matplotlib.pyplot as plt
import skimage.io as io
import os

def save_image_with_annotations(json_file_path, image_directory, image_id, output_directory):
    coco = COCO(json_file_path)
    
    # Load the image
    img_info = coco.loadImgs(image_id)[0]
    image_path = f'{image_directory}/{img_info["file_name"]}'
    image = io.imread(image_path)
    plt.figure(figsize=(10, 10))
    plt.imshow(image); plt.axis('off')
    
    # Load and display the annotations
    ann_ids = coco.getAnnIds(imgIds=img_info['id'], iscrowd=None)
    anns = coco.loadAnns(ann_ids)

    for ann in anns:
        if 'bbox' in ann:
            # Draw rectangle for bbox
            bbox = ann['bbox']
            rect = plt.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], linewidth=2, edgecolor='r', facecolor='none')
            plt.gca().add_patch(rect)

    # Ensure the output directory exists
    output_path = os.path.join(output_directory, "test.jpg")

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    plt.savefig(output_path)
    plt.close()

    print(f"Saved annotated image to {output_path}")

# Example usage:
json_file_path = '/rds/general/user/az2120/home/DeViT/devit/datasets/CUB_200_2011/annotations/cub200_coco_format.json'
image_directory = '/rds/general/user/az2120/home/DeViT/devit/datasets/CUB_200_2011/images'
image_id = random.randint(1,10000)
# Ensure you replace 'path_to_your_file.json', 'path_to_your_images', and 'path_to_output_dir' with actual paths
save_image_with_annotations(json_file_path, image_directory, image_id, output_directory='/rds/general/user/az2120/home/DeViT/devit')
