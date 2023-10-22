import logging
from vinepilot.model.model import TrackDetectionModel
from vinepilot.model.data import VinePilotDataloader, VinePilotDataset
from vinepilot.model.optimizer import VinePilotOptimizer
from vinepilot.model.loss import VinePilotLoss
from vinepilot.model.train import train


dataloader = VinePilotDataloader(dataset_class=VinePilotDataset)()
model = TrackDetectionModel()
optimizer = VinePilotOptimizer(trainable_parameters=model.parameters())()
loss = VinePilotLoss()()

train(dataloader, model, loss, optimizer)

