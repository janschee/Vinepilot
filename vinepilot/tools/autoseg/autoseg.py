import os
import cv2
import numpy as np
from vinepilot.config import Project


class AutoSeg():
    def __init__(self) -> None:
        self.objects: dict = {
            "dirt": [],
            "gras": [],
            "grapevines": [],
            "street": []
        }

        self.classes: dict = {
            
        }

    @staticmethod
    def rgb2lab(img: np.ndarray) -> np.ndarray:
        return np.array(cv2.cvtColor(img, cv2.COLOR_RGB2Lab))
    
    @staticmethod
    def lab2rgb(img: np.ndarray) -> np.ndarray:
        return np.array(cv2.cvtColor(img, cv2.COLOR_Lab2RGB))

    @staticmethod
    def normalize_luminace(lab_img: np.ndarray, L_value: int) -> np.ndarray:
        img: np.ndarray = lab_img
        img[:,:,0] = L_value
        return np.array(img)
    







