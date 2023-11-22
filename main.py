#!/home/jan/documents/Vinepilot/venv/bin/python

#from vinepilot.tools import VineyardViewer
#viewer = VineyardViewer()
#viewer.show()

from vinepilot.utils import Transform, load_image_as_numpy, save_numpy_image



test_img: str = "./vinepilot/data/vineyards/vineyard_000/vineyard_000.png"
target_img: str = "./vinepilot/data/vineyards/vineyard_000/target.png"

img = load_image_as_numpy(test_img)
new_center: tuple = (0.9, 0.9)
new_image = Transform.zoom(img=img, zoom_factor=2)
save_numpy_image(img_arr=new_image, path=target_img)