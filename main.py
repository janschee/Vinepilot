#!/home/jan/Vinepilot/venv/bin/python

#from vinepilot.tools import VineyardViewer
#viewer = VineyardViewer()
#viewer.show()

import os
import numpy as np
from torch.utils.data import DataLoader
from vinepilot.config import Project
from vinepilot.utils import save_numpy_image, torch2numpy_img
from vinepilot.model.train import train
from vinepilot.model.data import VinePilotSegmentationDataset
from vinepilot.model.model import SegmantationModel
from vinepilot.model.optimizer import VinePilotOptimizer
from vinepilot.model.loss import VinePilotLoss

test_video = os.path.join(Project.vineyards_dir, "./vineyard_000/vineyard_000.mp4")
target_img = os.path.join(Project.vineyards_dir, "./vineyard_000/target_000.png")
target2_img = os.path.join(Project.vineyards_dir, "./vineyard_000/target2_000.png")
target3_img = os.path.join(Project.vineyards_dir, "./vineyard_000/target3_000.png")

dataset = VinePilotSegmentationDataset()
dataloader = DataLoader(dataset, Project.batch_size, Project.shuffle)
model = SegmantationModel()
loss_fn = VinePilotLoss(loss= Project.loss)()
optimizer = VinePilotOptimizer(optimizer= Project.optimizer, learning_rate= Project.learning_rate, trainable_parameters= model.parameters())()

if __name__ == "__main__":
    train(dataloader, model, loss_fn, optimizer, Project.epochs)

    for i in range(0, dataset.__len__(), 100): 
        print("\n", "Freame:", i, )
        frame, seggray, segrgb = dataset.__getitem__(i)
        frame = torch2numpy_img(frame)
        seggray = torch2numpy_img(seggray)
        segrgb = torch2numpy_img(segrgb)
        save_numpy_image(frame, target_img)
        save_numpy_image(seggray, target2_img)
        save_numpy_image(segrgb, target3_img)

