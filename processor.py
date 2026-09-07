import torch
import json
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
        self.root = Path(path_data)
        with open(self.root / "_annotations.coco.json") as f:
            self.coco = json.load(f)

    def __len__(self):
        # Returns the length of a dataset
        return len(self.coco['images'])

    def __getitem__(self, index):
        img_info = self.coco["images"][index]
        full_path = self.root / img_info["file_name"]
        img = Image.open(full_path)
        return img






    


