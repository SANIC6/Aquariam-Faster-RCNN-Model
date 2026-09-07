
import torch
import json
import numpy as np
from pathlib import Path
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision.datasets import ImageFolder
from torchvision import transforms
import PIL.Image as Image


import logging
import pytest


logger = logging.getLogger(__name__)



class AquaDataset(Dataset):
    def __init__(self,path_data):
        super().__init__()
        #Intialize path_dir towards the model
        self.root = Path(path_data)
        with open(self.root / "_annotations.coco.json") as f:
            self.coco = json.load(f)

    def img_transforms(self,img):
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((224, 224))
        ])
        return transform(img)
        
    def __len__(self):
        # Returns the length of a dataset
        return len(self.coco['images'])
        
    def __getitem__(self, index):
        # Returns the image and its corresponding bounding box as a tensor
        img_info = self.coco["images"][index]
        image_id = self.coco['images'][index]["id"]
        full_path = self.root / img_info["file_name"]
        img = Image.open(full_path)
        bbox_list = []
        label_list = []
        areas = []
        is_crowds = []
        #Of the image it checks all classifications to it
        for annotation in self.coco["annotations"]:
            if annotation["image_id"] == image_id:
                bbox = annotation["bbox"]
                if len(bbox) == 4:                    
                    x_min = bbox[0]
                    y_min = bbox[1]
                    x_max = bbox[0] + bbox[2]
                    y_max = bbox[1] + bbox[3]
                    bbox = [x_min, y_min, x_max, y_max]
                else:
                    bbox = torch.tensor(bbox, dtype=torch.float32).view(-1, 4)
                label = annotation["category_id"]
                areas.append(annotation['area'])
                is_crowds.append(annotation['iscrowd'])
                bbox_list.append(bbox)
                label_list.append(label)
        #Label information as tensors
        bbox_tensor = torch.tensor(bbox_list, dtype=torch.float32)
        label_tensor = torch.tensor(label_list, dtype=torch.int64)
        area_tensor = torch.tensor(areas, dtype=torch.float32)
        iscrowd_tensor = torch.tensor(is_crowds, dtype=torch.int64)

        target = {}
        target["boxes"] = bbox_tensor
        target["labels"] = label_tensor
        target['image_id'] = torch.tensor([image_id])
        target['area'] = area_tensor
        target['iscrowd'] = iscrowd_tensor
        img = self.img_transforms(img)
        return img, target


test_Dataset = AquaDataset("data/Aquarium Combined/train")
