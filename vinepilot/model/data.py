import os
import logging
import json
import torch

from PIL import Image
from torchvision import transforms

from vinepilot.config import Project
from vinepilot.utils import check_points, sort_points

#Dataset
class VinePilotDataset(torch.utils.data.Dataset):
    def __init__(self):
        super().__init__()
        self.data: list[dict] = json.load(open(Project.data_path, "r"))
        self.image_to_tensor: function = transforms.ToTensor()

    def __len__(self):
        len_data: int = len(self.data)
        num_images: int = len(os.listdir(Project.image_dir))
        if len_data != num_images: logging.warning(f"There are {num_images} images, but  data has a length of {len_data}!")
        return len_data

    def __getitem__(self, idx):
        image_path: str = os.path.normpath(os.path.join(Project.image_dir, f"img_{str(idx+1).zfill(4)}.jpg"))
        image_tensor: torch.TensorType = self.image_to_tensor(Image.open(image_path))
        points: list = self.data[idx]["annotations"][0]["result"][1]["value"]["points"]
        is_valid: bool = check_points(idx+1, points)
        points: torch.TensorType = torch.Tensor(sort_points(points)) if is_valid else torch.Tensor([-1])
        return image_tensor, points, is_valid

#Dataloader
class VinePilotDataloader():
    def __init__(self, dataset_class) -> None:
        self.dataset = dataset_class()
        self.dataloader = torch.utils.data.DataLoader(dataset=self.dataset, batch_size=Project.batch_size, shuffle=Project.shuffle)

    def __call__(self):
        return self.dataloader
