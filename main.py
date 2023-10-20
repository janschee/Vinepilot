import logging
from vinepilot.model.data import VinePilotDataloader, VinePilotDataset
from vinepilot.config import Project
from vinepilot.utils import reorder_points


dataloader = VinePilotDataloader(VinePilotDataset)
for batch, (image, points, valid) in enumerate(dataloader()):
    if not valid: continue

    points = reorder_points(points)
    print(batch+1, points)

