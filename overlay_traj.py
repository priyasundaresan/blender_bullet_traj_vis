import cv2
import numpy as np
import os
from PIL import Image

def create_overlay(img_dir, alpha=0.3, skip_frames=1):
    result = None
    for i, fn in enumerate(sorted(os.listdir(img_dir))[::skip_frames]):
        img   = Image.open(os.path.join(img_dir, fn))
        if result is None:
            result = img
        else:
            result.paste(img, mask=img)
            result = Image.blend(result, img, alpha=alpha)
    result.save('result.png')

if __name__ == '__main__':
    img_dir = 'images' # Input image dir, created by Blender
    alpha = 0.5 # Transparency (between 0-1; 0 less and 1 is more opacity)
    skip_frames = 3 # Overlay every skip_frames
    create_overlay(img_dir, alpha=alpha, skip_frames=skip_frames)
