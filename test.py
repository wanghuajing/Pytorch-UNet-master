import pandas as pd
from shutil import copy
from PIL import Image
from PIL import ImageFilter
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import pydicom


def get_mask(image_address, mask_address, address):
    image = cv2.imread(image_address, -1)
    half = int(image.shape[1] / 2)
    left = image[:, :half]
    right = image[:, -half:]
    if right.sum() > left.sum():
        image = cv2.flip(image, 1)

    mask = cv2.imread(mask_address, -1)
    half = int(mask.shape[1] / 2)
    left = mask[:, :half]
    right = mask[:, -half:]
    if right.sum() > left.sum():
        mask = cv2.flip(mask, 1)

    mask=mask[:,:image.shape[1]]
    canny = cv2.Canny(mask, 30, 100)
    img = ((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img[canny == 255] = [0, 0, 255]
    cv2.imwrite(address, img)


image_dir = '/home/zhao/mydata/test/image/'
mask_dir = '/home/zhao/mydata/test/mask/'
image = os.listdir(image_dir)
mask = os.listdir(mask_dir)
for i in range(len(image)):
    get_mask(image_dir + image[i], mask_dir + mask[i], '/home/zhao/mydata/test/'+image[i])
