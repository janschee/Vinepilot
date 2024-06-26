#!/home/jan/Vinepilot/venv/bin/python

import numpy as np
from torch.utils.data import DataLoader
from vinepilot.config import Project
from vinepilot.model.train import train
from vinepilot.model.inference import inference
from vinepilot.model.data import VinePilotSegmentationDataset
from vinepilot.model.unet import UNet
from vinepilot.model.optimizer import VinePilotOptimizer
from vinepilot.model.loss import VinePilotLoss


dataset = VinePilotSegmentationDataset()
dataloader = DataLoader(dataset, Project.batch_size, Project.shuffle)
model = UNet(n_channels=1, n_classes=4)
loss_fn = VinePilotLoss(loss= Project.loss)()
optimizer = VinePilotOptimizer(optimizer= Project.optimizer, learning_rate= Project.learning_rate, trainable_parameters= model.parameters())()

if __name__ == "__main__":
    #train(dataloader, model, loss_fn, optimizer, Project.epochs)
    inference(dataset, model)

