import logging
import time
import cv2
import numpy as np
import torch
from vinepilot.config import Project

#TODO: change all image formats to (batch, channel, hight, width)

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
            "track": {"id": 1, "color": (0,0,255), "graytone": 100},
            "grapevine": {"id": 2, "color": (0,255,0), "graytone": 150},
            "driveway": {"id": 3, "color": (0,100,100), "graytone": 200},
            "none": {"id": 0, "color": (0,0,0), "graytone": 0}
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
        def func(pxl):
            l, a, b = np.array(pxl)
            l = int(l * 100/255)
            a = a - 128
            b = b - 128
            return (l, a, b)
        nimg: np.ndarray = np.apply_along_axis(func, 2, img)
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
        binary_mask = img
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
    
    def segmentation(self, img: np.ndarray) -> np.ndarray:
        def func(pxl):
                pred_class: str | None = self.classify_pixel(np.array(pxl), dist_function=self.lab_color_distance)
                return self.target_classes[pred_class]["id"] if pred_class is not None else self.target_classes["none"]["id"]
        segimg: np.ndarray = np.apply_along_axis(func, 2, img)
        return np.array(segimg).astype(np.uint8)

    def classwise_filter(self, img: np.ndarray, filters: list) -> np.ndarray:
        #Init
        class_names: list = []
        class_ids: list = []
        class_simgs: list = []
        for key, value in self.target_classes.items(): 
            class_names.append(key)
            class_ids.append(value["id"])
            class_simgs.append(np.zeros_like(img))
        #Split classes
        for i, idx in enumerate(class_ids): class_simgs[i] = np.where(img == idx, 1, 0).astype(np.uint8)
        #Filtering
        for filter in filters: class_simgs = [filter(i) for i in class_simgs]
        #Binary to ID image
        for i, simg in enumerate(class_simgs): class_simgs[i] = np.where(simg == 1, class_ids[i], 0)
        #Recombine classes
        fimg: np.ndarray = np.zeros_like(img)
        for simg in class_simgs: fimg = np.add(fimg, simg)
        return np.array(fimg)

    def seg2rgb(self, img: np.ndarray) -> np.ndarray:
        id_colors: list = sorted([[value["id"], value["color"]] for value in self.target_classes.values()], key=lambda x : x[0])
        rgb_colors: np.ndarray = np.array([x[1] for x in id_colors ])
        def func(pxl): return rgb_colors[pxl]
        rgbimg: np.ndarray = np.apply_along_axis(func, 1, img)
        return np.array(rgbimg).astype(np.uint8)
    
    def seg2gray(self, img: np.ndarray) -> np.ndarray:
        id_graytones: list = sorted([[value["id"], value["graytone"]] for value in self.target_classes.values()], key=lambda x : x[0])
        graytones: np.ndarray = np.array([x[1] for x in id_graytones])
        def func(pxl): return graytones[pxl]
        rgbimg: np.ndarray = np.apply_along_axis(func, 1, img)
        return np.array(rgbimg).astype(np.uint8)

    def gray2rgb(self, img: np.ndarray) -> np.ndarray:
        id_colors_gray: list = sorted([[value["id"], value["color"], value["graytone"]] for value in self.target_classes.values()], key=lambda x : x[0])
        rgb_colors: np.ndarray = np.array([x[1] for x in id_colors_gray])
        gray_colors: np.ndarray = np.array([x[2] for x in id_colors_gray])
        #def func1(pxl): return list(gray_colors).index(min(list(gray_colors), key=lambda x: abs(pxl-x)))
        #idimg: np.ndarray = np.apply_along_axis(func1, 1, npimg)
        idimg: np.ndarray = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint)
        #TODO: Try Optimize this loop!
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                idimg[i][j] = list(gray_colors).index(min(list(gray_colors), key=lambda x: abs(img[i][j]-x)))
        def func2(pxl): return rgb_colors[pxl]
        rgbimg: np.ndarray = np.apply_along_axis(func2, 1, idimg)
        return np.array(rgbimg).astype(np.uint8)

    def seg2multichannel(self, img: np.ndarray) -> np.ndarray:
        num_channels: int = len(self.target_classes)
        binary_tensor: np.ndarray = np.zeros((num_channels, img.shape[0], img.shape[1])) #Channel first format!
        for i in range(num_channels): binary_tensor[i] = np.where(img == i, 1, 0)
        return np.array(binary_tensor).astype(np.uint8)

    def multichannel2rgb(self, img: torch.TensorType) -> np.ndarray:
        idimg: torch.TensorType = torch.max(img, dim=0).indices
        return self.seg2rgb(idimg.numpy())




    def __call__(self, img: np.ndarray) -> np.ndarray:
        logging.debug(f"AutoSeg: Generating image...")
        start = time.time()

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

        #Convert to RGB
        x_gray = self.seg2gray(x)

        #Convert to RGB
        x_rgb = self.seg2rgb(x)

        #Convert to multi-channel
        x_multi = self.seg2multichannel(x)

        #Overlay
        #overlay = cv2.addWeighted(img, 0.5, x, 0.5, 0)
        end = time.time()
        logging.debug(f"AutoSeg: ...Done! ({end-start} sec.)")
        return np.array(x), np.array(x_gray), np.array(x_rgb), np.array(x_multi)



        




