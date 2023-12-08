import os
import cv2
import numpy as np
from vinepilot.config import Project


class AutoSeg():
    def __init__(self) -> None:
        self.classes: dict = {
            #Drivable Area
            "drivable": {
                #"dirt": [(111,89,66)],
                "grass": [(0,100,0)],
                #"asphalt": [(107,84,94)]
            },

            #Grapevines
            "grapevine": {
                "leaves": [(100,0,0)],
                #"trunk": [(83,94,105)],
                #"trellis": [(81,94,103)]
            }
        }

        self.colors: dict = {
            "drivable": (0,0,255),
            "grapevine": (0,255,0),
            "none": (0,0,0)
        }

    @staticmethod
    def rgb2lab(img: np.ndarray) -> np.ndarray:
        return np.array(cv2.cvtColor(img, cv2.COLOR_RGB2Lab))
    
    @staticmethod
    def lab2rgb(img: np.ndarray) -> np.ndarray:
        return np.array(cv2.cvtColor(img, cv2.COLOR_Lab2RGB))

    @staticmethod
    def normalize_luminace(lab_img: np.ndarray, L_value: int = 100) -> np.ndarray:
        img: np.ndarray = lab_img
        img[:,:,0] = L_value
        return np.array(img)
    
    @staticmethod
    def rgb_color_distance(rgb1: tuple, rgb2: tuple) -> float:
        return np.linalg.norm(abs(np.array(rgb1)-np.array(rgb2)))
    
    def classify_pixel(self, pxl: tuple, threshold: float) -> str | None:
        distances: list[str, float] = []
        for parent_class in self.classes:
            for sub_class in self.classes[parent_class]:
                distances.append([parent_class, self.rgb_color_distance(pxl, self.classes[parent_class][sub_class])])
        min_class, min_dist = min(distances, key=lambda x: x[1])
        if min_dist > threshold: return None
        return str(min_class)
    
    def __call__(self, img: np.ndarray) -> np.ndarray:
        #Normalize luminance
        x = self.rgb2lab(img)
        x = self.normalize_luminace(x)
        x = self.lab2rgb(x)

        #Segmentation
        segimg: np.ndarray = np.zeros_like(img)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                pred_class: str | None = self.classify_pixel(img[i][j], threshold=100)
                segimg[i][j] = self.colors[pred_class] if pred_class is not None else self.colors["none"]
        return np.array(segimg)



        




