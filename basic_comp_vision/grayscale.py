import WebGUI
import Frequency
import cv2 as cv
import numpy as np

while True:
    Frequency.tick()

    img = WebGUI.getImage()
    if img is None:
        continue

    img = np.asarray(img)

    # Case 1: Already grayscale
    if img.ndim == 2:
        gray = img

    # Case 2: Color image
    elif img.ndim == 3:
        # RGBA
        if img.shape[2] == 4:
            gray = cv.cvtColor(img, cv.COLOR_RGBA2GRAY)
        # BGR or RGB
        else:
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    else:
        continue  # unknown format

    WebGUI.showImage(gray)
