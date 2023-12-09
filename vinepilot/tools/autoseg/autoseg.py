import os
import cv2
import numpy as np
from vinepilot.config import Project


class AutoSeg():
    def __init__(self) -> None:
        
        #Classes (Lab colors)
        self.classes: dict = {
            #Track
            "track": {
                #"dirt": [(111,89,66)],
                "grass": [(57, -58, 58), 60],
            },

            #Grapevines
            "grapevine": {
                "leaves": [(54, 31, 56), 45],
                #"trunk": [(83,94,105)],
                #"trellis": [(81,94,103)]
            },

            #Driveway
            "driveway": {
                "asphalt": [(44, 12, -2), 10],
            }
        }

        self.colors: dict = {
            "track": (0,0,255),
            "grapevine": (0,255,0),
            "driveway": (0, 100, 100),
            "none": (0,0,0)
        }

    @staticmethod
    def rgb2lab(img: np.ndarray) -> np.ndarray:
        return np.array(cv2.cvtColor(img, cv2.COLOR_RGB2Lab))
    
    @staticmethod
    def lab2rgb(img: np.ndarray) -> np.ndarray:
        return np.array(cv2.cvtColor(img, cv2.COLOR_Lab2RGB))
    
    @staticmethod
    def normalize_lab(img: np.ndarray) -> np.ndarray:
        nimg: np.ndarray = np.zeros_like(img, dtype=int)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                l, a, b = img[i][j]
                l = int(l * 100/255)
                a = a - 128
                b = b - 128
                nimg[i][j] = [l,a,b]
        return np.array(nimg)
        
    @staticmethod
    def normalize_luminace(lab_img: np.ndarray, L_value: int = 100) -> np.ndarray:
        img: np.ndarray = lab_img
        img[:,:,0] = L_value
        return np.array(img)
    
    @staticmethod
    def median_filter(img: np.ndarray, size: int = 7) -> np.ndarray:
        return np.array(cv2.medianBlur(img, ksize = size))
    
    @staticmethod
    def lab_color_distance(lab1: tuple, lab2: tuple) -> float:
        return np.linalg.norm(abs(np.array(lab1)[1:]-np.array(lab2)[1:]))
    
    def classify_pixel(self, pxl: tuple) -> str | None:
        distances: list[str, float, int] = []
        for parent_class in self.classes:
            for sub_class in self.classes[parent_class]:
                lab, threshold = self.classes[parent_class][sub_class]
                distances.append([parent_class, self.lab_color_distance(pxl, lab), threshold])
        distances = sorted(distances, key=lambda x: x[1])
        for dist in distances:
            min_class, min_dist, min_threshold = dist
            if min_dist < min_threshold: return str(min_class)
        return None
    
    def segmentation(self, img: np.ndarray) -> np.ndarray:
        segimg: np.ndarray = np.zeros_like(img)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                pred_class: str | None = self.classify_pixel(img[i][j])
                segimg[i][j] = self.colors[pred_class] if pred_class is not None else self.colors["none"]
        return np.array(segimg).astype(np.uint8)

    
    def __call__(self, img: np.ndarray) -> np.ndarray:
        #Normalize luminance
        x = self.rgb2lab(img)
        x = self.normalize_lab(x)
        x = self.normalize_luminace(x)

        #Segmentation
        x = self.segmentation(x)

        #Filter
        x = self.median_filter(x)
        return np.array(x)



        




