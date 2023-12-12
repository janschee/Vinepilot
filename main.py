#!/home/jan/documents/Vinepilot/venv/bin/python

#from vinepilot.tools import VineyardViewer
#viewer = VineyardViewer()
#viewer.show()

import os
import time
from vinepilot.config import Project
from vinepilot.utils import save_numpy_image
from vinepilot.model.data import VinePilotSegmentationDataset

test_video = os.path.join(Project.vineyards_dir, "./vineyard_000/vineyard_000.mp4")
target_img = os.path.join(Project.vineyards_dir, "./vineyard_000/target_000.png")
target2_img = os.path.join(Project.vineyards_dir, "./vineyard_000/target2_000.png")

dataset = VinePilotSegmentationDataset()

for i in range(0, dataset.__len__(), 100): 
    print("Freame:", i, "\n")
    frame, segimg = dataset.__getitem__(i)
    save_numpy_image(frame, target_img)
    save_numpy_image(segimg, target2_img)
    time.sleep(2)

