
# -*- coding: utf-8 -*-
"""
# Author: Venkata Ravi Kumar A
# File name: faster_rcnn_config.py

"""

# path to your own data and coco file
train_data_dir = "UTSynData/train/images"
train_coco = "UTSynData/train/image_coco_annotations.json"

# Batch size
train_batch_size = 10

# Params for dataloader
train_shuffle_dl = True
num_workers_dl = 4

# Params for training

# Two classes; thistle class or background
num_classes = 2
num_epochs = 10

lr = 0.005
momentum = 0.9
weight_decay = 0.005