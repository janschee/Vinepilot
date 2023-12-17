#!/home/jan/Documents/Vinepilot/venv/bin/python

#from vinepilot.tools import VineyardViewer
#viewer = VineyardViewer()
#viewer.show()

import os
from torch.utils.data import DataLoader
from vinepilot.config import Project
from vinepilot.utils import save_numpy_image
from vinepilot.model.train import train
from vinepilot.model.data import VinePilotSegmentationDataset
from vinepilot.model.model import SegmantationModel
from vinepilot.model.optimizer import VinePilotOptimizer
from vinepilot.model.loss import VinePilotLoss

test_video = os.path.join(Project.vineyards_dir, "./vineyard_000/vineyard_000.mp4")
target_img = os.path.join(Project.vineyards_dir, "./vineyard_000/target_000.png")
target2_img = os.path.join(Project.vineyards_dir, "./vineyard_000/target2_000.png")

dataset = VinePilotSegmentationDataset()
dataloader = DataLoader(dataset, Project.batch_size, Project.shuffle)
model = SegmantationModel()
loss = VinePilotLoss()
optimizer = VinePilotOptimizer(trainable_parameters=model.parameters())

if __name__ == "__main__":
    train(dataloader, model, loss, optimizer, Project.epochs)

"""
for i in range(0, dataset.__len__(), 100): 
    print("Freame:", i, "\n")
    frame, segimg = dataset.__getitem__(i)
    save_numpy_image(frame, target_img)
    save_numpy_image(segimg, target2_img)
    print(segimg.shape)
    time.sleep(2)
"""



