import os
import logging
import json
import torch

import numpy as np

from PIL import Image
from torchvision import transforms

from vinepilot.config import Project
from vinepilot.utils import Transform, load_image_as_numpy, load_video_frame

class VinePilotSegmentationDataset(torch.utils.data.Dataset):
    def __init__(self) -> None:
        super().__init__()
        self.vineyard_number: int = 0 #TODO: Use as argument!

        #Paths
        self.vineyard_dir: str = os.path.normpath(os.path.join(Project.vineyards_dir, f"./vineyard_{str(self.vineyard_number).zfill(3)}"))
        self.base_img_path: str = os.path.normpath(os.path.join(self.vineyard_dir, f"./vineyard_{str(self.vineyard_number).zfill(3)}.png")) 
        self.video_path: str = os.path.normpath(os.path.join(self.vineyard_dir, f"./vineyard_{str(self.vineyard_number).zfill(3)}.mp4")) 
        self.trajectory_path: str = os.path.normpath(os.path.join(self.vineyard_dir, f"./trajectory_{str(self.vineyard_number).zfill(3)}.json"))

        #Misc
        self.trajectory: dict = json.load(open(self.trajectory_path, "r"))

    def overwrite_trajectory(self, new_trajectory: dict) -> None:
        self.trajectory = new_trajectory

    def get_item_by_frame(self, frame: int) -> tuple[np.ndarray, np.ndarray]:
        #Parameters
        zoom_factor: float = self.trajectory["zoom"]
        y_pos: float = self.trajectory["waypoints"][str(frame)]["position"][0]
        x_pos: float = self.trajectory["waypoints"][str(frame)]["position"][1]
        rotation: float = self.trajectory["waypoints"][str(frame)]["rotation"]

        #Virtual Image       
        vimg = load_image_as_numpy(self.base_img_path)
        vimg = Transform.new_center(vimg, [y_pos, x_pos])
        vimg = Transform.rotate(vimg, rotation)
        vimg = Transform.zoom(vimg, zoom_factor)
        vimg = Transform.crop_to_square(vimg)
        vimg = Transform.scale(vimg, (256, 256))

        #Create Mask
        #TODO: Fix mask!
        mask = np.zeros_like(vimg)
        for i in range(256): 
            for j in range(256): 
                if j <= i and j <= 255 - i: mask[i,j] = [1,1,1]
        vimg = vimg * mask

        #Real Image
        rimg = load_video_frame(video_path=self.video_path, frame=frame)
        rimg = Transform.scale(rimg, (200, 300))

        return rimg, vimg

    def __len__(self) -> int:
        with open(self.trajectory_path, "r") as f: trajectory = json.load(f)
        return len(trajectory["waypoints"])

    def __getitem__(self, idx: int):
        frame: int = list(self.trajectory["waypoints"].keys())[idx]
        return self.get_item_by_frame(frame)


"""
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
"""
