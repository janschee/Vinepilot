import os
import cv2
import numpy as np
from vinepilot.config import Project


class AutoSeg():
    def __init__(self) -> None:
        
        #Classes (Lab format)
        self.classes: dict = {
            #Track
            "track": {
                #"dirt": [(111,89,66)],
                "grass": [(57, -58, 58), 65], #Lab
                #"grass": [(29, 159, 4), 100], #rgb

            },

            #Grapevines
            "grapevine": {
                "leaves": [(54, 31, 56), 50], #Lab
                #"leaves": [(196, 105, 18), 100], #rgb
                #"trunk": [(83,94,105)],
                #"trellis": [(81,94,103)]
            },

            #Driveway
            "driveway": {
                "asphalt": [(44, 12, -2), 13], #lab
                #"asphalt": [(122, 97, 108), 35], #rgb
            }
        }

        #Segmentation colors (RGB format)
        self.target_classes: dict = {
            "track": {"id": 10, "color": (0,0,255)},
            "grapevine": {"id": 10, "color": (0,255,0)},
            "driveway": {"id": 10, "color": (0,100,100)},
            "none": {"id": 0, "color": (0,0,0)}
        }

    @staticmethod
    def rgb2lab(img: np.ndarray) -> np.ndarray:
        return np.array(cv2.cvtColor(img, cv2.COLOR_RGB2Lab))
    
    @staticmethod
    def lab2rgb(img: np.ndarray) -> np.ndarray:
        return np.array(cv2.cvtColor(img, cv2.COLOR_Lab2RGB))

    @staticmethod
    def rgb2bgr(img: np.ndarray) -> np.ndarray:
        return np.array(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    
    @staticmethod
    def bgr2rgb(img: np.ndarray) -> np.ndarray:
        return np.array(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

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
    
    @staticmethod
    def rgb_color_distance(rgb1: tuple, rgb2: tuple) -> float:
        return np.linalg.norm(abs(np.array(rgb1)-np.array(rgb2)))
    
    @staticmethod
    def area_size_filter(img: np.ndarray, threshold_area: int = 500):
        fimg: np.ndarray = img.copy()
        grayscale: np.ndarray = np.array(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY))
        _, binary_mask = cv2.threshold(grayscale, 1, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for con in contours:
            if cv2.contourArea(con) < threshold_area:
                cv2.drawContours(fimg, [con], 0, (0, 0, 0), thickness=cv2.FILLED)
        return np.array(fimg)


    def classify_pixel(self, pxl: tuple, dist_function: callable) -> str | None:
        distances: list[str, float, int] = []
        for parent_class in self.classes:
            for sub_class in self.classes[parent_class]:
                lab, threshold = self.classes[parent_class][sub_class]
                distances.append([parent_class, dist_function(pxl, lab), threshold])
        distances = sorted(distances, key=lambda x: x[1])
        for dist in distances:
            min_class, min_dist, min_threshold = dist
            if min_dist < min_threshold: return str(min_class)
        return None
    
    def segmentation(self, img: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        segimg_rgb: np.ndarray = np.zeros_like(img)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                pred_class: str | None = self.classify_pixel(img[i][j], dist_function=self.lab_color_distance)
                segimg_rgb[i][j] = self.target_classes[pred_class]["color"] if pred_class is not None else self.target_classes["none"]["color"]
        return np.array(segimg_rgb).astype(np.uint8)

    def classwise_filter(self, img: np.ndarray, filters: list) -> np.ndarray:
        #Init
        class_names: list = []
        class_values: list = []
        class_simgs: list = []
        for key, value in self.target_classes.items(): 
            class_names.append(key)
            class_values.append(value["color"])
            class_simgs.append(np.zeros_like(img))
        #Split classes
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                pxl = img[i][j]
                for idx, value in enumerate(class_values): 
                    if np.array_equal(pxl, value):
                        class_simgs[idx][i][j] = pxl
        #Filtering
        for filter in filters: class_simgs = [filter(i) for i in class_simgs]
        #Recombine classes
        fimg: np.ndarray = np.zeros_like(img)
        for simg in class_simgs: fimg = np.add(fimg, simg)
        return np.array(fimg)
    
    def __call__(self, img: np.ndarray) -> np.ndarray:
        #RGB2LAB
        x = self.rgb2lab(img)

        #Normalize luminance
        x = self.normalize_luminace(x)

        #Filter
        x = self.median_filter(x)
        x = self.median_filter(x)
        
        #Value space
        x = self.normalize_lab(x)

        #Segmentation
        x = self.segmentation(x)

        #Classwise Filter
        x = self.classwise_filter(x, filters=[
            self.median_filter,
            self.median_filter,
            self.area_size_filter,
            self.median_filter,
            self.median_filter,
        ])

        #Overlay
        overlay = cv2.addWeighted(img, 0.5, x, 0.5, 0)
        
        return np.array(x), np.array(overlay)



        




