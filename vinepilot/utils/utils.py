
from PIL import Image
import numpy as np
import cv2

def load_image_as_numpy(img_path: str) -> np.ndarray:
    return np.array(Image.open(img_path))

def save_numpy_image(img_arr: np.ndarray, path: str) -> None:
    npimg = np.array(img_arr).astype(np.uint8)
    if len(npimg.shape) == 3 and npimg.shape[2] == 1: npimg = np.squeeze(npimg, 2)
    npimg = np.clip(npimg, 0, 255).astype(np.uint8)
    img = Image.fromarray(npimg)
    img.save(path)

def save_torch_image(tensor, path: str) -> None:
    npimg = tensor.numpy()
    npimg = np.transpose(tensor, (1,2,0))
    save_numpy_image(npimg, path)

def load_video_frame(video_path: str, frame: int) -> np.ndarray:
    cap = cv2.VideoCapture(video_path)
    assert cap.isOpened(), "Could not open video file!"
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
    valid, data = cap.read()
    assert valid, "Unable to read frame!"
    data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
    cap.release()
    return np.array(data)

def total_video_frames(video_path: str) -> int:
    cap = cv2.VideoCapture(video_path)
    assert cap.isOpened(), "Could not open video file!"
    return int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
def torch2numpy_img(tensor) -> np.ndarray:
    npimg = tensor.numpy()
    npimg = np.transpose(tensor, (1,2,0))
    return np.array(npimg).astype(np.uint8)





