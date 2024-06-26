import os
import logging

import torch
import torchvision
import numpy as np

from vinepilot.config import Project
from vinepilot.tools import AutoSeg
from vinepilot.utils import Transform, load_video_frame, total_video_frames

class VinePilotSegmentationDataset(torch.utils.data.Dataset):
    def __init__(self) -> None:
        super().__init__()
        self.vineyard_number: int = 0 #TODO: Use as argument!

        #Paths
        self.vineyard_dir: str = os.path.normpath(os.path.join(Project.vineyards_dir, f"./vineyard_{str(self.vineyard_number).zfill(3)}"))
        self.video_path: str = os.path.normpath(os.path.join(self.vineyard_dir, f"./vineyard_{str(self.vineyard_number).zfill(3)}.mp4")) 

        #Misc
        self.autoseg = AutoSeg()
        self.input_resolution: tuple = (128,256)

    @staticmethod 
    def channel_first(tensor): return tensor.permute(2, 0, 1) #(height, width, channels) -> (channels, height, width)
 
    @staticmethod 
    def add_channel_dim(tensor): return tensor.unsqueeze(0) #(height, width) -> (channels, height, width)

    def __len__(self) -> int:
        return total_video_frames(self.video_path)

    def __getitem__(self, idx: int):
        logging.debug(f"Loading Frame {idx} from {self.video_path}.")
        frame: np.ndarray = load_video_frame(self.video_path, frame=idx)
        frame = Transform.scale(frame, self.input_resolution)
        segimg, seggray, segrgb, segmulti = self.autoseg(frame)
        frame = self.channel_first(torch.tensor(frame))
        frame = torchvision.transforms.Grayscale(num_output_channels=1)(frame)
        return torch.Tensor(frame), torch.Tensor(segimg), self.add_channel_dim(torch.Tensor(seggray)), self.channel_first(torch.tensor(segrgb)), torch.tensor(segmulti, dtype=torch.uint8)