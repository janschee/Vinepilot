import os
import logging
import json
import torch

from PIL import Image
from torchvision import transforms
from config import Project

class VineTrackDataset(torch.utils.data.Dataset):
    def __init__(self):
        self.data: list[dict] = json.load(open(Project.data_path, "r"))

    def __len__(self):
        len_data: int = len(self.data)
        num_images: int = len(os.listdir(Project.image_dir))
        if len_data != num_images: logging.warning(f"There are {num_images} images, but  data has a length of {len_data}!")
        return len_data

    def __getitem__(self, idx):
        assert idx != 0, logging.error("The dataset uses one-based indexing, but index 0 was requested!")
        image_path: str = os.path.normpath(os.path.join(Project.image_dir, f"img_{str(idx).zfill(4)}.jpg"))
        image_tensor: torch.TensorType = transforms.ToTensor(Image.open(image_path))
        print(image_tensor)

if __name__ == "__main__":
    dataset = VineTrackDataset()
    VineTrackDataset.__getitem__(2)