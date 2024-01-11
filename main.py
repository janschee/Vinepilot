#!/home/jan/Vinepilot/venv/bin/python

#from vinepilot.tools import VineyardViewer
#viewer = VineyardViewer()
#viewer.show()

import os
import numpy as np
import time
from torch.utils.data import DataLoader
from vinepilot.config import Project
from vinepilot.utils import save_numpy_image, save_torch_image, load_video_frame
from vinepilot.model.train import train
from vinepilot.model.inference import inference
from vinepilot.model.data import VinePilotSegmentationDataset
from vinepilot.model.unet import UNet
from vinepilot.model.optimizer import VinePilotOptimizer
from vinepilot.model.loss import VinePilotLoss
from vinepilot.tools import AutoSeg
from vinepilot.utils import Transform

test_video = os.path.join(Project.vineyards_dir, "./vineyard_000/vineyard_000.mp4")
frame_img = os.path.join(Project.vineyards_dir, "./vineyard_000/frame_000.png")
target_img = os.path.join(Project.vineyards_dir, "./vineyard_000/target_000.png")
target_rgb_img = os.path.join(Project.vineyards_dir, "./vineyard_000/target_rgb_000.png")

dataset = VinePilotSegmentationDataset()
dataloader = DataLoader(dataset, Project.batch_size, Project.shuffle)
model = UNet(n_channels=1, n_classes=4)
loss_fn = VinePilotLoss(loss= Project.loss)()
optimizer = VinePilotOptimizer(optimizer= Project.optimizer, learning_rate= Project.learning_rate, trainable_parameters= model.parameters())()

if __name__ == "__main__":
    #train(dataloader, model, loss_fn, optimizer, Project.epochs)
    inference(dataset, model)

    exit()
    for i in range(0, dataset.__len__(), 100): 
        print("\n", "Freame:", i, )
        #img, segimg, seggray, segrgb, segmulti = dataset.__getitem__(i)
        frame = load_video_frame(test_video, i)
        frame = Transform.scale(frame, (128, 256))
        _, _, segrgb, _, labimg = AutoSeg()(np.array(frame))
        save_numpy_image(labimg, target_img)
        save_numpy_image(segrgb, target_rgb_img)
        time.sleep(2)



        #save_torch_image(seggray, target_img)
        #save_torch_image(segrgb, target_rgb_img)

