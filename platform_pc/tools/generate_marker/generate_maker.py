import cv2 as cv
import numpy as np
import os

# Resolve output directory relative to this script (→ assets/markers/ at repo root)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', '..', 'assets', 'markers'))
os.makedirs(OUTPUT_DIR, exist_ok=True)

dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
marker_size = 200  # pixels

for marker_id in range(1, 4):
    img = cv.aruco.generateImageMarker(dictionary, marker_id, marker_size)
    out = os.path.join(OUTPUT_DIR, f'marker{marker_id}.png')
    cv.imwrite(out, img)
    print(f"Saved {out}")