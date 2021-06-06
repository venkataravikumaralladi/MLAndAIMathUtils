# -*- coding: utf-8 -*-
"""
Orginal author: Adam Kelly (Immersive Limit: https://www.immersivelimit.com/)
Adapter for Skymaps Author: Venkata Ravi Kumar A
# File name: faster_rcnn_utils.py
# References: https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch
#             https://www.immersivelimit.com/tutorials/composing-images-with-python-for-synthetic-datasets
#             https://www.immersivelimit.com/tutorials/cutting-out-image-foregrounds-with-gimp
"""

#!/usr/bin/env python3

# python imports
import os

# pytorch imports
import torch
import torch.utils.data
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

# image imports
from PIL import Image

# COCO imports
from pycocotools.coco import COCO



class SyntheticImageDataset(torch.utils.data.Dataset):
    
    def __init__(self, root, annotation, transforms=None):
        """ Initializes the class.
        Args:
            root: root path of annotation file.
            annotation: annotation file in coco format
            transforms: transforms function.
        """
        self.root = root
        self.transforms = transforms
        self.synth_img_coco_json = COCO(annotation)
        self.ids = list(sorted(self.synth_img_coco_json.imgs.keys()))

    def __getitem__(self, index):
        
        """ Used by dataloader to load images effectively during training.
        Args:
            index: index value of image to be retrived.
        """
        # Own coco file
        coco = self.synth_img_coco_json
        # get image details for current index.
        img_id = self.ids[index]
        ann_ids = coco.getAnnIds(imgIds=img_id)
        coco_annotation = coco.loadAnns(ann_ids)
        path = coco.loadImgs(img_id)[0]["file_name"]
        img = Image.open(os.path.join(self.root, path))
        num_objs = len(coco_annotation)

        # Bounding boxes for objects
        # In coco format, bbox = [xmin, ymin, width, height]
        # In pytorch, the input should be [xmin, ymin, xmax, ymax]
        boxes = []
        for i in range(num_objs):
            xmin = coco_annotation[i]["bbox"][0]
            ymin = coco_annotation[i]["bbox"][1]
            xmax = xmin + coco_annotation[i]["bbox"][2]
            ymax = ymin + coco_annotation[i]["bbox"][3]
            boxes.append([xmin, ymin, xmax, ymax])
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        # Labels (In synthetic data we have only one class: thisttle class or background)
        labels = torch.ones((num_objs,), dtype=torch.int64)
        # Tensorise img_id
        img_id = torch.tensor([img_id])
        # Size of bbox (Rectangular)
        areas = []
        for i in range(num_objs):
            areas.append(coco_annotation[i]["area"])
        areas = torch.as_tensor(areas, dtype=torch.float32)
        # Iscrowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

        # Annotation is in dictionary format
        img_annotation = {}
        img_annotation["boxes"] = boxes
        img_annotation["labels"] = labels
        img_annotation["image_id"] = img_id
        img_annotation["area"] = areas
        img_annotation["iscrowd"] = iscrowd

        if self.transforms is not None:
            img = self.transforms(img)

        return img, img_annotation

    def __len__(self):
        return len(self.ids)


# Utility functions.

def get_transform():
    custom_transforms = []
    custom_transforms.append(torchvision.transforms.ToTensor())
    return torchvision.transforms.Compose(custom_transforms)


# collate_fn needs for batch
def collate_fn(batch):
    return tuple(zip(*batch))


def get_faster_rcnn_model_instance_segmentation(num_classes):
    # load an instance segmentation model pre-trained pre-trained on COCO
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False)
    # get number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    return model