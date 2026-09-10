
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
        self.bbox_dict = {}
        self.label_dict = {}
        self.areas = {}
        self.is_crowds = {}
        self.bbox_list = []
        self.areas_list = []
        self.is_crowds_list = []
        self.labels = []
        last_img = None
        #Of the image it checks all classifications to it
        for annotation in self.coco["annotations"]:
            bbox = annotation["bbox"]
            image_id = annotation["image_id"]
            if len(bbox) == 4:                    
                x_min = bbox[0]
                y_min = bbox[1]
                x_max = bbox[0] + bbox[2]
                y_max = bbox[1] + bbox[3]

                bbox = [x_min, y_min, x_max, y_max]
            else:
                bbox = torch.empty((0,4))
            label = annotation["category_id"]
            areas = annotation['area']
            is_crowds = annotation['iscrowd']
            self.bbox_list.append(bbox)

            self.labels.append(label)
            self.areas_list.append(areas)
            self.is_crowds_list.append(is_crowds)
            self.areas[image_id] = self.areas_list
            self.is_crowds[image_id] = self.is_crowds_list
            self.bbox_dict[image_id] = self.bbox_list
            self.label_dict[image_id] = self.labels
            last_img = image_id

    def img_transforms(self,img):
        transform = transforms.Compose([
            transforms.ToTensor()
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
        img = Image.open(full_path).convert("RGB")
        bbox = self.bbox_dict[image_id]
        label = self.label_dict[image_id]
        target = {}
        target["boxes"] = torch.tensor(bbox)
        target["labels"] = torch.tensor(label)
        target['image_id'] = torch.tensor([image_id])
        target['area'] = torch.tensor(self.areas[image_id])
        target['iscrowd'] = torch.tensor(self.is_crowds[image_id])
        img = self.img_transforms(img)
        return img, target

def collate_fn(batch):
    return tuple(zip(*batch))


test_data = AquaDataset("C:/Users/somay/Pytorch/Aquariam/data/Aquarium Combined/train")
print(test_data[0])
test_data = AquaDataset("C:/Users/somay/Pytorch/Aquariam/data/Aquarium Combined/train")
print(test_data[0])