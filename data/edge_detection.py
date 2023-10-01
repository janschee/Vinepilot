import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys
import os

img_dir = sys.argv[1]
for img in os.listdir(img_dir)[:20]:
    img_path = f"{img_dir}{img}"
    print(img_path)


    #Detect
    img_data = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
    assert img_data is not None, "file could not be read, check with os.path.exists()"
    #edges = cv.Canny(img_data,100,200)
    edges = cv.Canny(img_data,200,600)

    #Plot
    plt.subplot(121),plt.imshow(img_data, cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges, cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.savefig(f"edges/{img}")
