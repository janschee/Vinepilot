import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import rotate as scipy_rotate
from scipy.ndimage import zoom as scipy_zoom


class Transform():
    @staticmethod
    def new_center(img: np.ndarray, new_center: tuple) -> np.ndarray:
        for i in new_center: assert i >= 0 and i <= 1, "Center position (row, coloumn) must be between 0 and 1!"
        img_shape_2D: np.ndarray = np.array(img.shape)[:2]
        new_center_absolute: np.ndarray = (np.array(new_center) * img_shape_2D).astype(int)
        offset: np.ndarray = new_center_absolute - img_shape_2D // 2
        new_img: np.ndarray = np.zeros((img_shape_2D[0]*2, img_shape_2D[1]*2, 3))
        new_origin: np.ndarray = np.array([img_shape_2D[0]//2 - offset[0], img_shape_2D[1]//2 - offset[1]])
        new_img[new_origin[0]:new_origin[0]+img_shape_2D[0], new_origin[1]:new_origin[1]+img_shape_2D[1]] = img
        new_img = new_img[img_shape_2D[0]//2:img_shape_2D[0]+img_shape_2D[0]//2, img_shape_2D[1]//2:img_shape_2D[1]+img_shape_2D[1]//2]
        return new_img.astype(np.uint8)

    @staticmethod
    def rotate(img: np.ndarray, angle: int) -> np.ndarray:
        return np.array(scipy_rotate(img, angle=angle, reshape=False, mode="constant", cval=0))

    @staticmethod
    def scale(img: np.ndarray, shape: tuple) -> np.ndarray:
        img_shape_2D: np.ndarray = np.array(img.shape)[:2]
        scale_factors: tuple = (shape[0]/img_shape_2D[0], shape[1]/img_shape_2D[1], 1)
        scaled_img: np.ndarray = np.array(scipy_zoom(img, scale_factors, order=3, mode="constant", cval=0))
        return scaled_img.astype(np.uint8)
        
    @staticmethod
    def zoom(img: np.ndarray, zoom_factor: float) -> np.ndarray:
        assert zoom_factor > 0, "Zoom factor must be larger than zero!"
        img_shape_2D: np.ndarray = np.array(img.shape)[:2]
        new_img_size: np.ndarray = np.array([int(img_shape_2D[0]/zoom_factor), int(img_shape_2D[1]/zoom_factor)])
        new_origin: np.ndarray = np.array([img_shape_2D[0]//2 - new_img_size[0]//2, img_shape_2D[1]//2 - new_img_size[1]//2])
        new_img = img[new_origin[0]:new_origin[0]+new_img_size[0], new_origin[1]:new_origin[1]+new_img_size[1]]
        new_img = Transform.scale(new_img, shape=tuple(img_shape_2D))
        return new_img.astype(np.uint8)

    @staticmethod
    def crop_to_square(img: np.ndarray) -> np.ndarray:
        img_shape_2D: np.ndarray = np.array(img.shape)[:2]
        assert img_shape_2D[0] != img_shape_2D[1], "Image already has square format!"
        crop_amount: int = abs(img_shape_2D[0]-img_shape_2D[1]) // 2
        if img_shape_2D[1] > img_shape_2D[0]: res: np.ndarray = img[:, crop_amount:(img_shape_2D[1]-crop_amount), :]
        else: res: np.ndarray = img[crop_amount:(img_shape_2D[0]-crop_amount), :, :]
        return res.astype(np.uint8)









