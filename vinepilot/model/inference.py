import logging
import os
import time
import torch
import torchvision
from vinepilot.tools import AutoSeg
from vinepilot.config import Project
from vinepilot.utils import Transform
from vinepilot.utils import save_torch_image, save_numpy_image, superimpose_images, torch2numpy_img, load_video_frame


#TODO: This seems a little out of place here. Find better solution!
test_video = os.path.join(Project.vineyards_dir, "./vineyard_000/vineyard_000.mp4")
frame_img = os.path.join(Project.vineyards_dir, "./vineyard_000/frame_000.png")
frame_gray_img = os.path.join(Project.vineyards_dir, "./vineyard_000/frame_gray_000.png")
target_img = os.path.join(Project.vineyards_dir, "./vineyard_000/target_000.png")
pred_img = os.path.join(Project.vineyards_dir, "./vineyard_000/pred_000.png")
pred_rgb_img = os.path.join(Project.vineyards_dir, "./vineyard_000/pred_rgb_000.png")

def inference(dataset, model):
    autoseg = AutoSeg()
    logging.info(f"Infer: Model Architecture: {model}")
    model.load_state_dict(torch.load(Project.model_weights))
    model.eval()
    with torch.no_grad():
        for i in range(0, dataset.__len__(), 100):
            logging.info(f"Infer: Predict frame {i}")
            img, segimg, seggray, segrgb, segmulti = dataset.__getitem__(i) #SLOW!

            video_frame = load_video_frame(test_video, i)
            video_frame = Transform.scale(video_frame, (128, 256)) 
            video_frame = torch.from_numpy(video_frame).permute(2,0,1)
            #video_frame = torchvision.transforms.Grayscale(num_output_channels=1)(img)

            #RGB frame
            save_torch_image(video_frame, frame_img)

            #Grayscale frame
            save_torch_image(img, frame_gray_img)

            #AutoSeg annotations
            save_torch_image(segrgb, target_img)

            #Predictions
            pred = model(img.unsqueeze(0).to(torch.float))
            pred = autoseg.multichannel2rgb(pred[0])
            overlay = superimpose_images(torch2numpy_img(img), pred)
            save_numpy_image(overlay, pred_img)


           


