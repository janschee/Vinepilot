#!/home/jan/documents/Vinepilot/venv/bin/python

#from vinepilot.tools import VineyardViewer
#viewer = VineyardViewer()
#viewer.show()

import os
from vinepilot.tools.autoseg import AutoSeg
from vinepilot.config import Project
from vinepilot.utils import load_video_frame, save_numpy_image, Transform

test_video = os.path.join(Project.vineyards_dir, "./vineyard_000/vineyard_000.mp4")
target_img = os.path.join(Project.vineyards_dir, "./vineyard_000/target_000.png")
target2_img = os.path.join(Project.vineyards_dir, "./vineyard_000/target2_000.png")

autoseg = AutoSeg()
img = load_video_frame(test_video, frame=0)
img = Transform.scale(img, (200,300))


seg, overlay = autoseg(img)

save_numpy_image(seg, target_img)
save_numpy_image(overlay, target2_img)

