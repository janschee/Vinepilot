import os
import logging
import json
import torch

from PIL import Image
from torchvision import transforms

from vinepilot.config import Project


class VinePilotDataloader(torch.utils.data.Dataset):
    def __init__(self):
        self.data: list[dict] = json.load(open(Project.data_path, "r"))
        self.image_to_tensor: function = transforms.ToTensor()

    def __len__(self):
        len_data: int = len(self.data)
        num_images: int = len(os.listdir(Project.image_dir))
        if len_data != num_images: logging.warning(f"There are {num_images} images, but  data has a length of {len_data}!")
        return len_data

    def __getitem__(self, idx):
        assert idx != 0, "The dataset uses one-based indexing, but index 0 was requested!"
        assert idx <= self.__len__(), "Requested index is bigger than the size of the dataset!"
        image_path: str = os.path.normpath(os.path.join(Project.image_dir, f"img_{str(idx).zfill(4)}.jpg"))
        image_tensor: torch.TensorType = self.image_to_tensor(Image.open(image_path))
        label: list = self.data[idx-1]["annotations"][0]["result"][1]["value"]["points"]
        return image_tensor, label
        
