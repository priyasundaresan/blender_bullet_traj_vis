import cv2
import numpy as np
import os
from PIL import Image

def overlay(img_dir):
    result = None
    alpha = 0.5
    for i, fn in enumerate(sorted(os.listdir(img_dir))[::2]):
    #for i, fn in enumerate(sorted(os.listdir(img_dir))):
        img   = Image.open(os.path.join(img_dir, fn))
        if result is None:
            result = img
        else:
            result.paste(img, mask=img)
            #result = Image.blend(result, img, alpha=.3)
            result = Image.blend(result, img, alpha=0.05)
    result.save('result.png')

if __name__ == '__main__':
    img_dir = 'images'
    overlay(img_dir)
