# -*- coding: utf-8 -*-
"""
# Author: Venkata Ravi Kumar A
# File name: faster_rcnn_train_main.py

"""

#!/usr/bin/env python3

import torch

import faster_rcnn_config

from faster_rcnn_utils import (
    get_faster_rcnn_model_instance_segmentation,
    collate_fn,
    get_transform,
    SyntheticImageDataset,
)

print("Torch version:", torch.__version__)

        
class ThisstleSynImageFasterRCNNTrainer:
    """
         Trains faster rcnn model with synthetic image.
    """

    def __init__(self):
        """ Initializes the class.
        Args:
            none
        """
        # initialize train data for training
        self.train_dataset = SyntheticImageDataset(root=faster_rcnn_config.train_data_dir,
                                                   annotation=faster_rcnn_config.train_coco,
                                                   transforms=get_transform())
        
        # create training DataLoader
        self.train_data_loader = torch.utils.data.DataLoader(self.train_dataset,
                                                             batch_size=faster_rcnn_config.train_batch_size,
                                                             shuffle=faster_rcnn_config.train_shuffle_dl,
                                                             num_workers=faster_rcnn_config.num_workers_dl,
                                                             collate_fn=collate_fn)
        
        # select device (whether GPU or CPU)
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        
        self.model = get_faster_rcnn_model_instance_segmentation(faster_rcnn_config.num_classes)
        return 
    
    def train(self):
        # move model to the right device
        self.model.to(self.device)
        
        # get parameters
        params = [p for p in self.model.parameters() if p.requires_grad]
        optimizer = torch.optim.SGD(params, lr=faster_rcnn_config.lr,
                                    momentum=faster_rcnn_config.momentum,
                                    weight_decay=faster_rcnn_config.weight_decay)
        len_dataloader = len(self.train_data_loader)

        # Training
        for epoch in range(faster_rcnn_config.num_epochs):
            print(f"Epoch: {epoch}/{faster_rcnn_config.num_epochs}")
            self.model.train()
            i = 0
            for imgs, annotations in self.train_data_loader:
                i += 1
                imgs = list(img.to(self.device) for img in imgs)
                annotations = [{k: v.to(self.device) for k, v in t.items()} for t in annotations]
                loss_dict = self.model(imgs, annotations)
                losses = sum(loss for loss in loss_dict.values())

                optimizer.zero_grad()
                losses.backward()
                optimizer.step()

            print(f"Epoch: {epoch}, Loss: {losses}")
            
        return
    
    def get_trained_model(self):
      print('returning trained model')
      return self.model
    
    