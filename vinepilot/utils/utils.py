import logging

from PIL import Image
import numpy as np

def load_image_as_numpy(img_path: str) -> np.ndarray:
    return np.array(Image.open(img_path))

def save_numpy_image(img_arr: np.ndarray, path: str) -> None:
    img = np.clip(img_arr, 0, 255).astype(np.uint8)
    img = Image.fromarray(img_arr)
    img.save(path)



