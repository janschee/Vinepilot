import os
import logging
import json
import yaml
import torch

class VineTrackDataset(torch.utils.data.Dataset):
    def __init__(self):
        self.this_file: str = os.path.abspath(__file__)
        self.base_dir: str = os.path.dirname(self.this_file)
        self.config_file: str = os.path.normpath(os.path.join(self.base_dir, "./config.yaml")) 
        self.config: dict = yaml.safe_load(open(self.config_file, "r"))
        self.image_dir: str = os.path.normpath(os.path.join(self.base_dir, self.config["dataset"]["image_dir"]))
        self.data_path: str = os.path.normpath(os.path.join(self.base_dir, self.config["dataset"]["data"]))
        self.data: list[dict] = json.load(open(self.data_path, "r"))

    def __len__(self):
        len_data: int = len(self.data)
        num_images: int = len(os.listdir(self.image_dir))
        if len_data != num_images: logging.warning(f"There are {num_images} images, but  data has a length of {len_data}!")
        return len_data

    def __getitem__(self, idx):
        assert idx != 0, logging.error("The dataset uses one-based indexing, but index 0 was requested!")
        