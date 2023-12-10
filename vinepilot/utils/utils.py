import logging
import math

from PIL import Image
import numpy as np
import cv2

def load_image_as_numpy(img_path: str) -> np.ndarray:
    return np.array(Image.open(img_path))

def save_numpy_image(img_arr: np.ndarray, path: str) -> None:
    img = np.clip(img_arr, 0, 255).astype(np.uint8)
    img = Image.fromarray(img_arr)
    img.save(path)

def load_video_frame(video_path: str, frame: int) -> np.ndarray:
    cap = cv2.VideoCapture(video_path)
    assert cap.isOpened(), "Could not open video file!"
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
    valid, data = cap.read()
    assert valid, "Unable to read frame!"
    data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
    return np.array(data)

def camera_angle_of_view(focal_length: float, sensor_size: float) -> float:
    angle_rad: float =  2 * math.atan(sensor_size/(2*focal_length))
    angle_deg: float = math.degrees(angle_rad)
    return  2 * angle_deg * (1920/1080)

    


