import pandas as pd
from shutil import copy
from PIL import Image
from PIL import ImageFilter
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

from skimage import exposure

path = '/home/zhao/mydata/data1/C_0001_1.LEFT_CC.png'
img = cv2.imread(path, -1)
img = img / img.max()
img = cv2.resize(img, (500, 800))
img = (img * 255).astype(np.uint8)
hist = cv2.calcHist([img], channels=[0], mask=None, histSize=[256], ranges=[0, 255])
plt.plot(hist, 'r')
plt.show()
img1 = cv2.equalizeHist(img)

# cv2.normalize(img1, img1, 0, 1, cv2.NORM_MINMAX)
cv2.imshow('1', img1)
cv2.waitKey()
cv2.destroyAllWindows()
